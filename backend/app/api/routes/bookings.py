from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.booking import BookingCreate, BookingResponse, BookingCancelResponse
from app.services.booking_service import book_seat
from app.crud.booking import get_user_bookings, get_all_bookings
from app.core.dependencies import get_current_user, admin_required

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingResponse)
def create_booking_route(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return book_seat(db, booking.flight_id, user["sub"])

@router.get("/me", response_model=list[BookingResponse])
def my_bookings(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    from app.models.booking import Booking
    from app.models.flight import Flight

    results = (
        db.query(
            Booking.id,
            Booking.user_email,
            Booking.flight_id,
            Booking.seat_id,
            Booking.booked_at,
            Booking.payment_status,
            Flight.flight_number,
            Flight.origin,
            Flight.destination,
        )
        .join(Flight, Booking.flight_id == Flight.id)
        .filter(Booking.user_email == user["sub"])
        .all()
    )

    # Convert to list of dicts matching BookingResponse
    return [
        {
            "id": r[0],
            "user_email": r[1],
            "flight_id": r[2],
            "seat_id": r[3],
            "booked_at": r[4],
            "payment_status": r[5],
            "flight_number": r[6],
            "origin": r[7],
            "destination": r[8],
        }
        for r in results
    ]

@router.get("/", response_model=list[BookingResponse], dependencies=[Depends(admin_required)])
def all_bookings(db: Session = Depends(get_db)):
    return get_all_bookings(db)


@router.delete("/{booking_id}", response_model=BookingCancelResponse)
def cancel_booking_route(
    booking_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    from app.services.booking_service import cancel_booking
    return cancel_booking(db, booking_id, user["sub"])
