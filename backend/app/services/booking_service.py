from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.booking import Booking
from app.models.seat import Seat

from app.crud.seat import get_available_seat
from app.crud.booking import create_booking

def book_seat(db: Session, flight_id: int, user_email: str):
    seat = get_available_seat(db, flight_id)
    if not seat:
        raise HTTPException(status_code=400, detail="No seats available")

    # TEMPORARY HOLD
    seat.is_booked = True

    booking = create_booking(
        db=db,
        user_email=user_email,
        flight_id=flight_id,
        seat_id=seat.id,
        payment_status="PENDING"
    )

    db.commit()
    return booking


# def book_seat(db: Session, flight_id: int, user_email: str):
#     seat = get_available_seat(db, flight_id)
#     if not seat:
#         raise HTTPException(status_code=400, detail="No seats available")
    
#     seat.is_booked = True
#     db.commit()

#     return create_booking(db, user_email, flight_id, seat.id)


def cancel_booking(db: Session, booking_id: int, user_email: str):
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_email == user_email
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    seat = db.query(Seat).filter(Seat.id == booking.seat_id).first()
    if seat:
        seat.is_booked = False

    db.delete(booking)
    db.commit()

    return {"message": "Booking cancelled successfully"}