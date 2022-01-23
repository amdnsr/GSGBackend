from datetime import datetime, timedelta

from typing import Any, Tuple, Union
from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.settings.app_settings import Settings

# taken from minimal-fastapi-postgres-template
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(subject: Union[str, Any]) -> Tuple[str, datetime]:
    now = datetime.utcnow()
    expire = now + timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expire, "sub": str(subject), "refresh": False}
    encoded_jwt: str = jwt.encode(
        to_encode,
        Settings.SECRET_KEY,
        algorithm=Settings.ALGORITHM,
    )
    return encoded_jwt, expire


def create_refresh_token(subject: Union[str, Any]) -> Tuple[str, datetime]:
    now = datetime.utcnow()
    expire = now + timedelta(minutes=Settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expire, "sub": str(subject), "refresh": True}
    encoded_jwt: str = jwt.encode(
        to_encode,
        Settings.SECRET_KEY,
        algorithm=Settings.ALGORITHM,
    )
    return encoded_jwt, expire

# taken from a different source (incompetent ian)


def decode_token(token):
    try:
        payload = jwt.decode(token, Settings.SECRET_KEY,
                             algorithms=Settings.ALGORITHM)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail='Invalid token')


bearer = HTTPBearer()


def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(bearer)):
    return decode_token(auth.credentials)

# taken from minimal-fastapi-postgres-template


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def is_refresh_token(token):
    try:
        payload = jwt.decode(token, Settings.SECRET_KEY,
                             algorithms=Settings.ALGORITHM)
        return payload['refresh']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail='Invalid token')
