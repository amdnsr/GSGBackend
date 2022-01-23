from datetime import datetime

from typing import List, Optional
from pydantic import BaseModel


class BookingQueryRequest(BaseModel):
    source: str
    destination: str
    date_of_journey: str


class SingleBusResult(BaseModel):
    bus_id: str
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
    result: List[SingleBusResult]


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


class CurrentSeatsAvlRequest(BaseModel):
    bus_id: str
    date: str
    source: str
    destination: str


class CurrentSeatsAvlResponse(BaseModel):
    avl_seats: int


class ForgotPasswordRequest:
    email: str
    new_password: str


"""agency endpoints models"""


class EachBusFromAgency:
    bus_name: str
    bus_number: str
    list_of_stops: List[str]
    # ("%H:%M:%S") like this
    departure_time: str
    # day=1,hour=5,minute=35 something like that
    # or H:M like that H ca be more than 24
    # time delta can be parsed day=H//24, H=H%24, M=M
    list_of_arrival_duration_from_src: List[str]
    base_fare: float
    list_of_fare_from_source: List[float]
    total_seat: int
    # SMTWTFS->TTFTFFT like this it will be simple string
    schedule: str


class AddAgencyDetailsRequest:
    agency_name: str
    agency_contact_number: str
    agency_email: str
    agency_address_street: str
    agency_address_city: str
    agency_address_state: str
    agency_address_pincode: str
    agency_bank_details: str
    list_of_bus: List[EachBusFromAgency]


class UpdateBusDetailRequest(EachBusFromAgency):
    bus_id: str


class DeleteBusDetailRequest:
    bus_id: str
