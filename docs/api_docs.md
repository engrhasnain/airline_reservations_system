# API Documentation

This document summarizes the main REST endpoints for the Airline Reservation System. Each entry is concise — check the codebase (`app/api/routes` and `app/schemas`) for full request/response shapes.

Authentication
- `POST /auth/register` — Create a new user. Body: `{ full_name, email, password }`. Returns created user metadata.
- `POST /auth/login` — Authenticate and receive a JWT. Body: `{ email, password }`. Returns `{ access_token, token_type }`.

Users
- `GET /users/me` — Return the current user's profile. Requires `Authorization: Bearer <token>`.

Flights
- `POST /flights/` — (admin) Create a flight (FlightCreate). Returns created flight.
- `GET /flights/` — List available flights (pagination via `skip`, `limit`).
- `GET /flights/search?origin=&destination=` — Search flights by origin and destination (partial matches allowed).
- `GET /flights/search/for?origin=&destination=&date=` — Search flights on a specific date and with available seats (`date` format: `YYYY-MM-DD`).
- `GET /flights/stats` — (admin) Booking counts grouped by flight.

Bookings
- `POST /bookings/` — Create a booking for an available flight. Requires auth. Body: `{ flight_id }`.
- `GET /bookings/me` — List bookings for the authenticated user.
- `GET /bookings/` — (admin) List all bookings.
- `DELETE /bookings/{booking_id}` — Cancel the specified booking (auth required).

Payments
- `POST /payments/` — Process a payment for a booking. Body: `{ booking_id, amount }`.

Tickets
- `GET /tickets/{booking_id}` — Generate or retrieve a ticket for a paid booking (auth required).

Admin
- `GET /admin/stats` — Return basic admin statistics (users, bookings).

Notes
- Protected endpoints expect `Authorization: Bearer <token>`.
- Many routes are implemented as placeholders — review their route files to see what remains to be implemented and to capture exact request/response models.
