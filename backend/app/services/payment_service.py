from sqlalchemy.orm import Session
from app.models.payment import Payment, PaymentStatus
from app.models.booking import Booking
from fastapi import HTTPException

# def process_payment(db: Session, booking_id: int, amount: int):
#     booking = db.query(Booking).filter(Booking.id == booking_id).first()
#     if not booking:
#         raise HTTPException(status_code=404, detail="Booking not found")

#     payment = Payment(
#         booking_id=booking_id,
#         amount=amount,
#         status=PaymentStatus.SUCCESS  # MOCK SUCCESS
#     )

#     booking.payment_status = "PAID"

#     db.add(payment)
#     db.commit()
#     db.refresh(payment)

#     return payment


def process_payment(db: Session, booking_id: int, amount: int):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    booking.payment_status = "PAID"

    payment = Payment(
        booking_id=booking_id,
        amount=amount,
        status=PaymentStatus.SUCCESS
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment
