from typing import List
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
