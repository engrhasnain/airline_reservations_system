from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.flight import FlightCreate, FlightResponse, FlightResponses
from app.crud.flight import create_flight, get_all_flights, search_flights
from app.core.dependencies import admin_required
from app.services.flight_service import search_flights_service

router = APIRouter(prefix="/flights", tags=["Flights"])

@router.post("/", response_model=FlightResponse, dependencies=[Depends(admin_required)])
def add_flight(flight: FlightCreate, db: Session = Depends(get_db)):
    return create_flight(db, flight)

@router.get("/", response_model=list[FlightResponse])
def list_flights(db: Session = Depends(get_db)):
    return get_all_flights(db)

@router.get("/search", response_model=list[FlightResponse])
def search(origin: str, destination: str, db: Session = Depends(get_db)):
    return search_flights(db, origin, destination)



from fastapi import Query
@router.get("/search/for", response_model=list[FlightResponses])
def search_flights(
    origin: str = Query(...),
    destination: str = Query(...),
    date: str = Query(...),
    db: Session = Depends(get_db)
):
    
    return search_flights_service(db, origin, destination, date)



@router.get("/stats", dependencies=[Depends(admin_required)])
def flight_stats(db: Session = Depends(get_db)):
    from sqlalchemy import func
    from app.models.booking import Booking
    from app.models.flight import Flight

    results = (
        db.query(
            Flight.flight_number,
            func.count(Booking.id).label("total_bookings")
        )
        .outerjoin(Booking)
        .group_by(Flight.flight_number)
        .all()
    )
    
    # Convert tuples to list of dictionaries
    return [
        {"flight_number": flight_number, "total_bookings": total_bookings}
        for flight_number, total_bookings in results
    ]