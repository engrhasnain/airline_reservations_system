from fastapi import APIRouter
from app.api.routes import auth, flights, bookings, tickets, payment, users, admin

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(flights.router)
api_router.include_router(bookings.router)
api_router.include_router(tickets.router)
api_router.include_router(payment.router)
api_router.include_router(admin.router)

