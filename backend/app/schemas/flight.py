from pydantic import BaseModel
from datetime import datetime

class FlightCreate(BaseModel):
    flight_number: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    total_seats: int

class FlightResponse(FlightCreate):
    id: int


class FlightResponses(BaseModel):
    id: int
    flight_number: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime

    class Config:
        from_attributes = True
