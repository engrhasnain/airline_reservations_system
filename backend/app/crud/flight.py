from sqlalchemy.orm import Session
from app.models.flight import Flight
from app.schemas.flight import FlightCreate
from app.crud.seat import create_seats

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
