# Airline Reservation System

This repository contains a sample Airline Reservation System with a FastAPI backend and a simple static frontend.

Structure:
- backend — FastAPI application and database models
- frontend — static frontend skeleton
- docs — project docs and API documentation
- docker — Dockerfile and docker-compose configuration

Next steps: implement endpoints, write tests, and wire up migrations.

## API Endpoints (current)

Authentication
- `POST /auth/register` — Register a new user (creates account).
- `POST /auth/login` — Authenticate a user and return a JWT access token.

Users (module present; not included in `api_router`)
- `GET /users/me` — Retrieve the currently authenticated user's profile (placeholder).

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

Payments (module present; not included in `api_router`)
- `POST /payments/` — Process a payment for a booking (expects `booking_id` and `amount`).

Tickets (module present; not included in `api_router`)
- `GET /tickets/{booking_id}` — Retrieve or generate a ticket for a paid booking (authentication required).

Admin (module present; not included in `api_router`)
- `GET /admin/stats` — Basic admin stats (users/bookings).

> Note: Protected endpoints expect a Bearer token in the `Authorization` header. Admin-only endpoints use the `admin_required` dependency.
