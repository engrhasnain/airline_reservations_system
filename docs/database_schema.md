# Database Schema

Overview
This project uses SQLAlchemy models to represent the main domain entities. Below are the primary tables, key fields, and relationships.

Tables
- `users` — id (PK), full_name, email (unique), hashed_password, is_admin (bool), created_at
- `flights` — id (PK), flight_number, origin, destination, departure_time (datetime), arrival_time (datetime), total_seats
- `seats` — id (PK), seat_number, flight_id (FK → `flights.id`), is_available (bool)
- `bookings` — id (PK), user_id (FK → `users.id`), flight_id (FK → `flights.id`), seat_id (FK → `seats.id`), booked_at (datetime), payment_status (optional)

Relationships
- One `Flight` has many `Seat` rows (Flight 1 - * Seats)
- One `Flight` can have many `Booking` records (Flight 1 - * Bookings)
- One `User` can have many `Booking` records (User 1 - * Bookings)
- A `Seat` is typically booked by a single `Booking` (Seat 1 - 0|1 Booking)

Simple ASCII ER
```
Users(id) 1---* Bookings(booking_id) *---1 Flights(id)
Flights(id) 1---* Seats(id)
``` 

Migrations
Use Alembic to manage schema changes; add migration scripts under `backend/alembic/` when altering models.
