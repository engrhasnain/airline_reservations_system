"""Business logic for seats (placeholder)"""
from ..crud import seat as seat_crud


def available_seats(db, flight_id):
    return seat_crud.list_available_seats(db, flight_id=flight_id)
