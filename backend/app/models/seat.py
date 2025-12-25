from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    seat_number = Column(Integer, nullable=False)
    is_booked = Column(Boolean, default=False)
    flight_id = Column(Integer, ForeignKey("flights.id"))

    flight = relationship("Flight")
