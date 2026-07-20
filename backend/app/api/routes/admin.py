from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import admin_required
from app.models.user import User
from app.models.booking import Booking

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/stats", dependencies=[Depends(admin_required)])
def stats(db: Session = Depends(get_db)):
    return {
        "users": db.query(User).count(),
        "bookings": db.query(Booking).count(),
    }
