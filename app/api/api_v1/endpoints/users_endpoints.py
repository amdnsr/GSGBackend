
from logging import error
from fastapi import Depends, HTTPException, status
from fastapi_utils.inferring_router import InferringRouter
from typing import Union
from app.models.request_response_models import CreateAccountRequest, CreateAccountResponse, LoginRequest, LoginResponse, UserProfileResponse
from app.core import security
from app.utils.email_utils import generate_new_account_token, send_new_account_email, verify_new_account_token
from app.db.mongo_insertion_handlers import user_details_insertion_handler

router = InferringRouter(tags=["users"])


@router.post("/register", response_model=Union[str, CreateAccountResponse])
def register(user: CreateAccountRequest):
    email = user.email
    first_name = user.first_name
    db_obj = user_details_insertion_handler.insert(user)
    token = generate_new_account_token(email)
    send_new_account_email(email, first_name, token)
    return f"Check your mail for confirmation of account. Your temporary id is {db_obj.id}"


@router.get("/confirm-account-creation")
def confirm_account(token: str):
    # print(token)
    if verify_new_account_token(token):
        return "Congratulations, you successfully activated your account!"
    else:
        return status.HTTP_401_UNAUTHORIZED


@router.post("/login", response_model=LoginResponse)
def login(login_details: LoginRequest):
    print(login_details)
    # hash the password and then check this in the users database

    # user = [object of a User class] # it has user_id, email and hashed_password (can also directly be the model in the db)
    # if user is None:
    #     raise HTTPException(status_code=400, detail="Incorrect email or password")

    # if not security.verify_password(login_details.password, user.hashed_password):  # type: ignore
    #     raise HTTPException(status_code=400, detail="Incorrect email or password")

    # access_token, expire_at = security.create_access_token(user.user_id)
    access_token, expire_at = security.create_access_token("ABC123")
    print(access_token, expire_at)
    # refresh_token, refresh_expire_at = security.create_refresh_token(user.user_id)
    refresh_token, refresh_expire_at = security.create_refresh_token("ABC123")

    return {
        "token_type": "bearer",
        "access_token": access_token,
        "expire_at": expire_at,
        "refresh_token": refresh_token,
        "refresh_expire_at": refresh_expire_at,
    }


@router.get("/profile/me", response_model=UserProfileResponse)
def get_profile(user_id: str = Depends(security.auth_wrapper)):
    print(user_id)
