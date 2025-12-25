"""Business logic for flights (placeholder)"""
# from ..crud import flight as flight_crud

from app.crud import flight as flight_crud


from sqlalchemy.orm import Session
from app.models.flight import Flight
from app.models.seat import Seat
from sqlalchemy import func



def list_flights(db, skip=0, limit=100):
    return flight_crud.list_flights(db, skip=skip, limit=limit)



def search_flights_service(db: Session, origin: str, destination: str, date: str):
    """Search flights by origin, destination and date.

    Minimal behavior: match flights by calendar date (YYYY-MM-DD). If an ISO datetime
    is provided, only the date portion is considered.
    """
    # Ensure db is a Session
    if not hasattr(db, "query"):
        raise TypeError("db must be a SQLAlchemy Session object")

    # Accept either 'YYYY-MM-DD' or an ISO datetime like 'YYYY-MM-DDTHH:MM', but
    # only use the date portion for matching
    date_only = date.split('T')[0] if date else date

    flights = (
        db.query(Flight)
        .join(Seat, Seat.flight_id == Flight.id)
        .filter(
            Flight.origin.ilike(f"%{origin}%"),
            Flight.destination.ilike(f"%{destination}%"),
            func.date(Flight.departure_time) == date_only,
            Seat.is_booked == False,
        )
        .all()
    )

    return flights
