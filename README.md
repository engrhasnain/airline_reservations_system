# Airline Reservation System

This repository contains a sample Airline Reservation System with a FastAPI backend and a simple static frontend.

Structure:
- backend — FastAPI application and database models
- frontend — static frontend skeleton
- docs — project docs and API documentation

Next steps: implement endpoints

Frontend (React)
- A minimal Vite + React app is scaffolded under `frontend/react-app`.
- To run locally:
  - cd `frontend/react-app`
  - npm install
  - npm run dev (opens on port 3000, proxies `/api` to backend `http://localhost:8000`)

Backend (FastAPI)
- Create a Python virtual environment and install requirements:
  - python -m venv venv
  - venv\Scripts\activate (Windows)
  - pip install -r backend/requirements.txt
- Configure `.env` in `backend/.env` (DATABASE_URL, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES)

Email / SMTP (optional)
- The app can send emails (login OTP, cancellation/refund notifications) when SMTP is configured.
- Add SMTP variables to `backend/.env`:
  - `SMTP_HOST` (e.g. `smtp.gmail.com`)
  - `SMTP_PORT` (e.g. `465` for SMTPS or `587` for STARTTLS)
  - `SMTP_USER` (email address)
  - `SMTP_PASSWORD` (SMTP password or app password)
  - `SMTP_USE_SSL` (`1` for SMTPS, `0` for STARTTLS)
  - `EMAIL_FROM` (optional, defaults to `SMTP_USER`)
- Example (SMTPS):
  ```dotenv
  SMTP_HOST=smtp.gmail.com
  SMTP_PORT=465
  SMTP_USER=your-email@example.com
  SMTP_PASSWORD=your-app-password
  SMTP_USE_SSL=1
  EMAIL_FROM=your-email@example.com
  ```
- After editing `.env`, restart the backend to pick up new settings.

- Run the app:
  - cd backend
  - uvicorn app.main:app --reload
- Run tests:
  - pytest backend/app/tests

Docker
- A Dockerfile and docker-compose.yml are provided under `docker/` for containerized runs.


## API Endpoints (current)

Authentication
- `POST /auth/register` — Register a new user (creates account).
- `POST /auth/login` — Authenticate a user and return a JWT access token.

Flights (included)
- `POST /flights/` — (admin) Create a new flight.
- `GET /flights/` — List all flights.
- `GET /flights/search?origin=&destination=` — Search flights by origin and destination.
- `GET /flights/search/for?origin=&destination=&date=` — Search flights for a specific date (filters by seat availability).
- `GET /flights/stats` — (admin) Aggregate booking statistics per flight.

Bookings (included)
- `POST /bookings/` — Create a booking for an available flight (authentication required).
- `GET /bookings/me` — List bookings for the authenticated user.
- `GET /bookings/` — (admin) List all bookings.
- `DELETE /bookings/{booking_id}` — Cancel a specific booking (authentication required).

Payments (module present; included in `api_router`)
- `POST /payments/` — Process a payment for a booking (expects `booking_id` and `amount`).

Tickets (module present; not included in `api_router`)
- `GET /tickets/{booking_id}` — Retrieve or generate a ticket for a paid booking (authentication required).

Admin (module present; included in `api_router`)
- `GET /admin/stats` — Basic admin stats (users/bookings).

> Note: Protected endpoints expect a Bearer token in the `Authorization` header. Admin-only endpoints use the `admin_required` dependency.
