from sqlalchemy.orm import Session
from app.models.booking import Booking

def create_booking(db: Session, user_email: str, flight_id: int, seat_id: int, payment_status: str):
    booking = Booking(
        user_email=user_email,
        flight_id=flight_id,
        seat_id=seat_id,
        payment_status = payment_status
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

def get_user_bookings(db: Session, email: str):
    return db.query(Booking).filter(Booking.user_email == email).all()

def get_all_bookings(db: Session):
    return db.query(Booking).all()
