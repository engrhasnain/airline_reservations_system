from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.booking import Booking
from app.models.seat import Seat

from app.crud.seat import get_available_seat
from app.crud.booking import create_booking

def book_seat(db: Session, flight_id: int, user_email: str):
    # Prevent duplicate booking for same user & flight
    from app.models.booking import Booking
    from sqlalchemy import or_
    # Only consider active/non-cancelled bookings when checking for duplicates
    existing = db.query(Booking).filter(
        Booking.user_email == user_email,
        Booking.flight_id == flight_id,
        or_(Booking.status != 'CANCELLED', Booking.status == None)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already has a booking for this flight")

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

    # send booking confirmation email (best-effort)
    try:
        from app.services.email_service import send_email
        from app.models.flight import Flight
        f = db.query(Flight).filter(Flight.id == flight_id).first()
        seat_obj = db.query(Seat).filter(Seat.id == seat.id).first()
        body = f"Your booking #{booking.id} for flight {f.flight_number} ({f.origin} → {f.destination}) on {f.departure_time} has been created. Seat: {seat_obj.seat_number}."
        send_email(user_email, "Booking confirmed", body)
    except Exception:
        pass

    return booking


# def book_seat(db: Session, flight_id: int, user_email: str):
#     seat = get_available_seat(db, flight_id)
#     if not seat:
#         raise HTTPException(status_code=400, detail="No seats available")
    
#     seat.is_booked = True
#     db.commit()

#     return create_booking(db, user_email, flight_id, seat.id)


from app.models.payment import Payment, PaymentStatus

def cancel_booking(db: Session, booking_id: int, user_email: str):
    # Ensure `status` column exists in bookings table (dev convenience - add column if missing)
    try:
        from sqlalchemy import inspect, text
        engine = db.get_bind()
        inspector = inspect(engine)
        cols = [c['name'] for c in inspector.get_columns('bookings')]
        if 'status' not in cols:
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE bookings ADD COLUMN status VARCHAR DEFAULT 'ACTIVE'"))
                conn.commit()
    except Exception:
        # best-effort; if this fails, we'll surface a DB error later
        pass

    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_email == user_email
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    payments = db.query(Payment).filter(Payment.booking_id == booking.id).all()

    # Check for any successful payments. We will mark the booking as REFUNDED (no direct DB enum mutation to avoid enum type migration complexities)
    had_success = False
    for p in payments:
        if p.status == PaymentStatus.SUCCESS:
            had_success = True

    # If there were no successful payments, clear any pending/failed payments
    if not had_success:
        for p in payments:
            db.delete(p)

    # update booking status and payment status
    seat = db.query(Seat).filter(Seat.id == booking.seat_id).first()
    if seat:
        seat.is_booked = False

    if had_success:
        booking.payment_status = "REFUNDED"

    booking.status = "CANCELLED"

    # capture email to notify
    notify_email = booking.user_email
    flight_id = booking.flight_id

    db.commit()

    # send cancellation & refund email (best-effort)
    try:
        from app.services.email_service import send_email
        body = f"Your booking #{booking.id} for flight {flight_id} has been cancelled."
        if had_success:
            body += " A refund has been issued to your original payment method."
        send_email(notify_email, "Booking cancelled", body)
    except Exception:
        pass

    return {"message": "Booking cancelled successfully", "refunded": had_success}