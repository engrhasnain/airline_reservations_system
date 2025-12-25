from sqlalchemy.orm import Session
from app.models.seat import Seat

def create_seats(db: Session, flight_id: int, total_seats: int):
    seats = [
        Seat(seat_number=i + 1, flight_id=flight_id)
        for i in range(total_seats)
    ]
    db.add_all(seats)
    db.commit()

def get_available_seat(db: Session, flight_id: int):
    return db.query(Seat).filter(
        Seat.flight_id == flight_id,
        Seat.is_booked == False
    ).first()
