from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.flight import FlightCreate, FlightResponse, FlightResponses, FlightDetail
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


@router.get("/{flight_id}/seats")
def flight_seats(flight_id: int, db: Session = Depends(get_db)):
    from app.models.seat import Seat

    seats = db.query(Seat.id, Seat.seat_number, Seat.is_booked).filter(Seat.flight_id == flight_id).all()
    return [{"id": s[0], "seat_number": s[1], "is_booked": s[2]} for s in seats]


@router.get("/{flight_id}", response_model=FlightDetail)
def get_flight_detail(flight_id: int, db: Session = Depends(get_db)):
    from sqlalchemy import func
    from app.models.seat import Seat
    from app.models.flight import Flight
    from fastapi import HTTPException

    flight = db.query(Flight).filter(Flight.id == flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    total = db.query(func.count(Seat.id)).filter(Seat.flight_id == flight_id).scalar() or 0
    available = db.query(func.count(Seat.id)).filter(Seat.flight_id == flight_id, Seat.is_booked == False).scalar() or 0

    return {
        "id": flight.id,
        "flight_number": flight.flight_number,
        "origin": flight.origin,
        "destination": flight.destination,
        "departure_time": flight.departure_time,
        "arrival_time": flight.arrival_time,
        "total_seats": total,
        "seats_available": available,
        "status": flight.status,
    }


@router.delete("/{flight_id}", dependencies=[Depends(admin_required)])
def delete_flight(flight_id: int, db: Session = Depends(get_db)):
    from fastapi import HTTPException
    from app.crud.flight import delete_flight

    # Verify exists
    from app.models.flight import Flight
    flight = db.query(Flight).filter(Flight.id == flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    return delete_flight(db, flight_id)


@router.patch("/{flight_id}/status", dependencies=[Depends(admin_required)])
def patch_flight_status(flight_id: int, status: str, db: Session = Depends(get_db)):
    from fastapi import HTTPException
    from app.crud.flight import update_flight_status

    flight = update_flight_status(db, flight_id, status)
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flight