
from logging import error
from fastapi import Depends, HTTPException, status
from fastapi_utils.inferring_router import InferringRouter
from app.models.request_response_models import CreateAccountRequest, CreateAccountResponse, LoginRequest, LoginResponse, UserProfileResponse
from app.core import security


router = InferringRouter(tags=["users"])


@router.post("/register", response_model=CreateAccountResponse)
def register(user_details: CreateAccountRequest):
    user_dict = user_details.dict()
    print(user_dict)


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
