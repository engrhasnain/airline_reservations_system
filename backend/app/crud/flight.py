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
    return db.query(Flight).all()

def search_flights(db: Session, origin: str, destination: str):
    return db.query(Flight).filter(
        Flight.origin == origin,
        Flight.destination == destination
    ).all()

def delete_flight(db: Session, flight_id: int):
    # Remove dependent bookings and seats
    db.query(Booking).filter(Booking.flight_id == flight_id).delete()
    db.query(Seat).filter(Seat.flight_id == flight_id).delete()
    db.query(Flight).filter(Flight.id == flight_id).delete()
    db.commit()
    return {"message": "Flight deleted"}

def update_flight_status(db: Session, flight_id: int, status: str):
    flight = db.query(Flight).filter(Flight.id == flight_id).first()
    if not flight:
        return None
    flight.status = status
    db.commit()
    return flight
