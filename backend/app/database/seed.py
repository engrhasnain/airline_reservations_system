"""Populate a handful of sample flights and a default admin account on first run."""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.flight import Flight
from app.models.user import User
from app.crud.seat import create_seats
from app.core.security import hash_password

DEFAULT_ADMIN_EMAIL = "admin@airlinedemo.com"
DEFAULT_ADMIN_PASSWORD = "admin123"

SAMPLE_FLIGHTS = [
    {"flight_number": "PK-101", "origin": "Karachi", "destination": "Lahore", "days_from_now": 1, "hour": 8, "duration_hours": 2, "total_seats": 40},
    {"flight_number": "PK-202", "origin": "Lahore", "destination": "Karachi", "days_from_now": 1, "hour": 14, "duration_hours": 2, "total_seats": 40},
    {"flight_number": "PK-303", "origin": "Karachi", "destination": "Islamabad", "days_from_now": 2, "hour": 9, "duration_hours": 2, "total_seats": 30},
    {"flight_number": "PK-404", "origin": "Islamabad", "destination": "Karachi", "days_from_now": 2, "hour": 18, "duration_hours": 2, "total_seats": 30},
    {"flight_number": "PK-505", "origin": "Lahore", "destination": "Islamabad", "days_from_now": 3, "hour": 7, "duration_hours": 1, "total_seats": 25},
    {"flight_number": "EK-101", "origin": "Karachi", "destination": "Dubai", "days_from_now": 4, "hour": 2, "duration_hours": 3, "total_seats": 60},
    {"flight_number": "EK-202", "origin": "Dubai", "destination": "Karachi", "days_from_now": 5, "hour": 23, "duration_hours": 3, "total_seats": 60},
    {"flight_number": "QR-303", "origin": "Lahore", "destination": "Doha", "days_from_now": 6, "hour": 4, "duration_hours": 4, "total_seats": 50},
    {"flight_number": "TK-404", "origin": "Islamabad", "destination": "Istanbul", "days_from_now": 7, "hour": 10, "duration_hours": 7, "total_seats": 45},
    {"flight_number": "PA-111", "origin": "Karachi", "destination": "London", "days_from_now": 10, "hour": 1, "duration_hours": 9, "total_seats": 55},
]


def seed_flights(db: Session):
    if db.query(Flight).first():
        return

    now = datetime.utcnow()
    for spec in SAMPLE_FLIGHTS:
        departure = (now + timedelta(days=spec["days_from_now"])).replace(
            hour=spec["hour"], minute=0, second=0, microsecond=0
        )
        arrival = departure + timedelta(hours=spec["duration_hours"])

        flight = Flight(
            flight_number=spec["flight_number"],
            origin=spec["origin"],
            destination=spec["destination"],
            departure_time=departure,
            arrival_time=arrival,
            total_seats=spec["total_seats"],
            status="ACTIVE",
        )
        db.add(flight)
        db.commit()
        db.refresh(flight)
        create_seats(db, flight.id, flight.total_seats)


def seed_admin(db: Session):
    if db.query(User).filter(User.is_admin == True).first():
        return

    db.add(User(
        full_name="Admin",
        email=DEFAULT_ADMIN_EMAIL,
        hashed_password=hash_password(DEFAULT_ADMIN_PASSWORD),
        is_admin=True,
    ))
    db.commit()
