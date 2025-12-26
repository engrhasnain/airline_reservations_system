from sqlalchemy.orm import Session
from app.models.flight import Flight
from app.schemas.flight import FlightCreate
from app.crud.seat import create_seats
from app.models.seat import Seat
from app.models.booking import Booking

def create_flight(db: Session, flight: FlightCreate):
    db_flight = Flight(**flight.dict())
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)

    create_seats(db, db_flight.id, db_flight.total_seats)
    return db_flight

def get_all_flights(db: Session):
    # Exclude cancelled flights from general listings
    from sqlalchemy import or_
    return db.query(Flight).filter(or_(Flight.status != 'CANCELLED', Flight.status == None)).all()

def search_flights(db: Session, origin: str, destination: str):
    from sqlalchemy import or_
    return db.query(Flight).filter(
        Flight.origin == origin,
        Flight.destination == destination,
        or_(Flight.status != 'CANCELLED', Flight.status == None)
    ).all()

def delete_flight(db: Session, flight_id: int):
    # Remove dependent payments, bookings and seats safely
    from app.models.payment import Payment

    # collect booking ids for this flight
    booking_ids = [r[0] for r in db.query(Booking.id).filter(Booking.flight_id == flight_id).all()]
    if booking_ids:
        # delete payments referencing those bookings first to avoid FK constraint errors
        db.query(Payment).filter(Payment.booking_id.in_(booking_ids)).delete(synchronize_session=False)

    db.query(Booking).filter(Booking.flight_id == flight_id).delete(synchronize_session=False)
    db.query(Seat).filter(Seat.flight_id == flight_id).delete(synchronize_session=False)
    db.query(Flight).filter(Flight.id == flight_id).delete(synchronize_session=False)
    db.commit()
    return {"message": "Flight deleted"}

def update_flight_status(db: Session, flight_id: int, status: str):
    flight = db.query(Flight).filter(Flight.id == flight_id).first()
    if not flight:
        return None
    flight.status = status
    db.commit()

    # If flight is cancelled, mark associated bookings as CANCELLED and refund payments (best-effort)
    if status == 'CANCELLED':
        from app.models.booking import Booking
        from app.models.payment import Payment, PaymentStatus
        from app.models.seat import Seat
        from app.services.email_service import send_email

        bookings = db.query(Booking).filter(Booking.flight_id == flight_id).all()
        for b in bookings:
            # unbook seat
            seat = db.query(Seat).filter(Seat.id == b.seat_id).first()
            if seat:
                seat.is_booked = False

            # handle payments
            payments = db.query(Payment).filter(Payment.booking_id == b.id).all()
            had_success = False
            for p in payments:
                if p.status == PaymentStatus.SUCCESS:
                    # mark refunded
                    try:
                        p.status = PaymentStatus.REFUNDED
                    except Exception:
                        # fallback: set as string on booking
                        pass
                    had_success = True
                else:
                    db.delete(p)

            if had_success:
                b.payment_status = 'REFUNDED'
            b.status = 'CANCELLED'

            # send notification email (best-effort)
            try:
                send_email(b.user_email, 'Flight cancelled', f'Your booking #{b.id} for flight {flight.flight_number} has been cancelled by the airline. A refund has been issued if applicable.')
            except Exception:
                pass

        db.commit()

    return flight
