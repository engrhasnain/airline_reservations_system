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

    class Config:
        orm_mode = True

class BookingCancelResponse(BaseModel):
    message: str