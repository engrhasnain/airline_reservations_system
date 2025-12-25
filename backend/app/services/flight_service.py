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
    flights = (
        db.query(Flight)
        .join(Seat)
        .filter(
            Flight.origin.ilike(origin),
            Flight.destination.ilike(destination),
            func.date(Flight.departure_time) == date,
            Seat.is_booked == False
        )
        .all()
    )

    return flights
