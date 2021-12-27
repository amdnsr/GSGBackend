from datetime import datetime

from typing import List, Optional
from pydantic import BaseModel


class BookingQueryRequest(BaseModel):
    source: str
    destination: str
    date_of_journey: str


class SingleQueryResult(BaseModel):
    source: str
    destination: str
    date_of_journey: str
    bus_number: str
    bus_name: str
    agency_name: str
    no_of_seats_available: int
    departure_time: str
    arrival_time: str
    fare_for_one_seat: float


class BookingQueryResponse(BaseModel):
    result: List[SingleQueryResult]


class CreateAccountRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    password: str
    confirm_password: str


class CreateAccountResponse(BaseModel):
    pass


class LoginRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    token_type: str
    access_token: str
    expire_at: datetime
    refresh_token: str
    refresh_expire_at: datetime


class TokenPayload(BaseModel):
    exp: datetime
    sub: Optional[str] = None
    refresh: Optional[bool] = None


class TokenRefresh(BaseModel):
    refresh_token: str


class LoginResponse(Token):
    pass


class UserProfileResponse(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
