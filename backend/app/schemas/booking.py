from pydantic import BaseModel
from datetime import datetime

class BookingCreate(BaseModel):
    flight_id: int

class BookingResponse(BaseModel):
    id: int
    user_email: str
    flight_id: int
    seat_id: int
    booked_at: datetime
    payment_status: str
    status: str
    flight_number: str | None = None
    origin: str | None = None
    destination: str | None = None

    class Config:
        orm_mode = True

class BookingCancelResponse(BaseModel):
    message: str