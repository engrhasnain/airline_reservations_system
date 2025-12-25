from pydantic import BaseModel

class SeatResponse(BaseModel):
    id: int
    seat_number: int
    is_booked: bool

    class Config:
        orm_mode = True
