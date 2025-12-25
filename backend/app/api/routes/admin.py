from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/stats")
def stats():
    return {"users": 0, "bookings": 0}
