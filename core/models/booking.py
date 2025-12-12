from pydantic import BaseModel
from typing import Optional
from datetime import date


class BookingDates(BaseModel):
    checkin: date
    checkout: date


class Booking(BaseModel): # название параметра должны точно совпадать в парметрами в ответе, который ждем
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: Optional[str] = None # это Необязательный параметр


class BookingResponse(BaseModel): # BaseModel -это базовая модель Pydantic
    bookingid: int
    booking: Booking
