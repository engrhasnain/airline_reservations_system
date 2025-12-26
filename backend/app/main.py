from fastapi import FastAPI
from app.core.config import settings
from app.database.session import engine
from app.database.base import Base
from app.api.api_router import api_router

# Import models so SQLAlchemy sees them
from app.models import user, flight, seat, booking, password_reset



Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Airline Reservation System API running"}
