from pydantic import BaseModel
from datetime import datetime

class TicketResponse(BaseModel):
    ticket_number: str
    flight_number: str
    source: str
    destination: str
    departure_time: datetime
    seat_number: int
    passenger_email: str

    class Config:
        from_attributes = True
