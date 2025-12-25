import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.models.flight import Flight
from app.models.seat import Seat

def generate_ticket(db: Session, booking_id: int, user_email: str):
    booking = (
        db.query(Booking)
        .filter(Booking.id == booking_id, Booking.user_email == user_email)
        .first()
    )

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.payment_status != "PAID":
        raise HTTPException(status_code=400, detail="Payment required")

    flight = db.query(Flight).filter(Flight.id == booking.flight_id).first()
    seat = db.query(Seat).filter(Seat.id == booking.seat_id).first()

    return {
        "ticket_number": str(uuid.uuid4())[:8],
        "flight_number": flight.flight_number,
        "source": flight.origin,
        "destination": flight.destination,
        "departure_time": flight.departure_time,
        "seat_number": seat.seat_number,
        "passenger_email": booking.user_email,
    }
