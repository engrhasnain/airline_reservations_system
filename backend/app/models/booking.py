from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, nullable=False)
    flight_id = Column(Integer, ForeignKey("flights.id"))
    seat_id = Column(Integer, ForeignKey("seats.id"))
    booked_at = Column(DateTime, default=datetime.utcnow)
    payment_status = Column(String, default="PENDING")
    status = Column(String, default="ACTIVE")

    flight = relationship("Flight")
    seat = relationship("Seat")
