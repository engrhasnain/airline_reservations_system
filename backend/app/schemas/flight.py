from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FlightCreate(BaseModel):
    flight_number: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    total_seats: int
    status: Optional[str] = "ACTIVE"

class FlightResponse(FlightCreate):
    id: int


class FlightResponses(BaseModel):
    id: int
    flight_number: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    status: str

    class Config:
        from_attributes = True


class FlightDetail(BaseModel):
    id: int
    flight_number: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    total_seats: int
    seats_available: int
    status: str

    class Config:
        orm_mode = True
        from_attributes = True
