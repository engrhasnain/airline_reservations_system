from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services.payment_service import process_payment

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/", response_model=PaymentResponse)
def make_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db)
):
    return process_payment(db, payment.booking_id, payment.amount)
