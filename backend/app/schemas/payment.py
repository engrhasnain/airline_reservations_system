from pydantic import BaseModel

class PaymentCreate(BaseModel):
    booking_id: int
    amount: int

class PaymentResponse(BaseModel):
    id: int
    booking_id: int
    status: str

    class Config:
        from_attributes = True
