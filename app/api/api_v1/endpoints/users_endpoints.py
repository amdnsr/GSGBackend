import imp
import os
from logging import error
import re
from fastapi import Depends, Form, HTTPException, Request, status
from fastapi_utils.inferring_router import InferringRouter
from fastapi.templating import Jinja2Templates

from typing import Union
from app.models.request_response_models import CreateAccountRequest, CreateAccountResponse, LoginRequest, LoginResponse, UserProfileResponse
from app.core import security
from app.utils.email_utils import generate_new_account_token, generate_password_reset_token, send_new_account_email, send_reset_password_email, verify_new_account_token, verify_password_reset_token
from app.db.mongo_insertion_handlers import user_details_insertion_handler
from app.db.mongo_retrieval_handlers import user_details_retrieval_handler
from app.service.mongo_service import MongoService
from app.exceptions.exceptions import ExpiredSignatureError_Exception, InvalidJWTToken_Exception
from app.config.configurations import AppConfig
from app.utils.helpers import FlaskJinjaSession

router = InferringRouter(tags=["users"])
template_dir_path = os.path.join(AppConfig.app_root_dir, "templates")
templates = Jinja2Templates(directory=template_dir_path)


@router.post("/register", response_model=Union[CreateAccountResponse, str])
def register(user: CreateAccountRequest):
    email = user.email
    print(email)

    # TODO
    # currently, mongo atlas is very slow, so checking for existing user takes a lot of time. Maybe it is because we are making a connection to db everytime?
    # instead maybe we should declare some global connections during the start of the program, and use their alias later?

    # Commenting it out for testing purpose
    # TODO remove the comments
    # existing_user = user_details_retrieval_handler.get_user_details_by_email(
    #     email)
    existing_user = MongoService.get_user_details_by_email(email)
    print("existing_user = ", existing_user)
    if existing_user:
        return "Sorry, an account already exists with this email!"
    first_name = user.first_name
    # db_obj = user_details_insertion_handler.insert(user)
    db_obj = MongoService.add_new_user(user)
    print("inserted user into db")
    token = generate_new_account_token(email)
    if not send_new_account_email(email, first_name, token):
        MongoService.delete_user(email)
        print("removed user from db")
        return f"Unable to send email to this address, please check your email again!"
    return f"Check your mail for confirmation of account. Your user id is {db_obj.id}"


@router.get("/confirm-account-creation")
def confirm_account(token: str):
    # print(token)
    try:
        email = verify_new_account_token(token)
    except ExpiredSignatureError_Exception:
        return "The confirmation link has expired!"
    except InvalidJWTToken_Exception:
        return "The token is invalid!"

    if email:
        try:
            MongoService.verify_user_email(email)
            return "Congratulations, you successfully activated your account!"
        except:
            return status.HTTP_304_NOT_MODIFIED
    else:
        return status.HTTP_401_UNAUTHORIZED


@router.post("/login", response_model=Union[LoginResponse, str])
def login(login_request: LoginRequest):
    email = login_request.email
    result = MongoService.validate_user_login(login_request)
    if not result:
        return "Sorry, wrong username/password!"

    # hash the password and then check this in the users database

    # user = [object of a User class] # it has user_id, email and hashed_password (can also directly be the model in the db)
    # if user is None:
    #     raise HTTPException(status_code=400, detail="Incorrect email or password")

    # if not security.verify_password(login_details.password, user.hashed_password):  # type: ignore
    #     raise HTTPException(status_code=400, detail="Incorrect email or password")

    # access_token, expire_at = security.create_access_token(user.user_id)
    access_token, expire_at = security.create_access_token(email)
    # refresh_token, refresh_expire_at = security.create_refresh_token(user.user_id)
    refresh_token, refresh_expire_at = security.create_refresh_token(email)

    return {
        "token_type": "bearer",
        "access_token": access_token,
        "expire_at": expire_at,
        "refresh_token": refresh_token,
        "refresh_expire_at": refresh_expire_at,
    }


@router.get("/profile/me", response_model=Union[UserProfileResponse, str])
def get_profile(email: str = Depends(security.auth_wrapper)):
    # user = user_details_retrieval_handler.get_user_details_by_email(email)
    user = MongoService.get_user_details_by_email(email)
    if not user:
        return "Sorry your account does not exist!"
    return user


@router.delete("/profile/delete", response_model=str)
def delete_profile(email: str = Depends(security.auth_wrapper)):
    if MongoService.delete_user(email):
        return "Successfully deleted the account!"
    return "Deletion unsuccessful!"


@router.post("/request-new-access-token")
def request_new_access_token(token):
    try:
        email = security.decode_token(token)
        is_refresh = security.is_refresh_token(token)
    except:
        return "Invalid token!"
    access_token, expire_at = security.create_access_token(email)
    return {
        "token_type": "bearer",
        "access_token": access_token,
        "expire_at": expire_at,
    }


@router.post("/request-reset-password")
def request_reset_password(email: str):
    print(f"got reset password request for {email}")
    token = generate_password_reset_token(email)
    if not send_reset_password_email(to_email=email, email=email, username=email, token=token):
        return "Unable to send email to this address, please check your email again!"
    return "Check your email for further instructions!"


@router.get("/reset-password")
def get_reset_password(token):
    try:
        verify_password_reset_token(token)
    except:
        return "Wrong token!"

    return templates.TemplateResponse("reset_password.html", {"token": token, "request": dict(), "session": FlaskJinjaSession()})


@router.post("/reset-password")
def reset_password(request: Request, token: str = Form(...), new_password: str = Form(...), confirm_new_password: str = Form(...)):
    if new_password != confirm_new_password:
        return "Passwords do not match!"

    try:
        email = verify_password_reset_token(token)
    except:
        return "Sorry, wrong token!"
    if MongoService.reset_user_password(email, new_password):
        return "Successfully changed the password!"
    return "Sorry, could not change the password!"


@router.get("/update-password")
def get_update_password(token: str):
    try:
        email = security.decode_token(token)
        return templates.TemplateResponse("update_password.html", {"token": token, "request": dict(), "session": FlaskJinjaSession()})
    except:
        return "Sorry, invalid token!"


@router.post("/update-password")
def update_password(token: str = Form(...), old_password: str = Form(...), new_password: str = Form(...), confirm_new_password: str = Form(...)):
    if new_password != confirm_new_password:
        return "Passwords do not match!"
    try:
        email = security.decode_token(token)
    except:
        return "Sorry, wrong token!"
    if MongoService.update_user_password(email, old_password, new_password):
        return "Successfully changed the password!"
    return "Sorry, could not change the password!"
