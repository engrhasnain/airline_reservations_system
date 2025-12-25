# from app.database.session import get_db
# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.core.dependencies import get_current_user
# from app.models.booking import Booking
# from fastapi import HTTPException
# from app.services.tickets_service import generate_ticket

# router = APIRouter()

# @router.get("/{booking_id}")
# def download_ticket(
#     booking_id: int,
#     db: Session = Depends(get_db),
#     user=Depends(get_current_user)
# ):
#     booking = db.query(Booking).filter(Booking.id == booking_id).first()

#     if booking.payment_status != "PAID":
#         raise HTTPException(status_code=400, detail="Payment required")

#     return generate_ticket(booking)


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.tickets import TicketResponse
from app.services.tickets_service import generate_ticket
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.get("/{booking_id}", response_model=TicketResponse)
def get_ticket(
    booking_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return generate_ticket(db, booking_id, user["sub"])
