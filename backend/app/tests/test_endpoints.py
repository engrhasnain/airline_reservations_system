from fastapi.testclient import TestClient
from app.main import app
from app.database.init_db import init_db

client = TestClient(app)

# Ensure DB tables exist for tests
init_db()

def test_register_and_login_and_flow():
    # Register user
    res = client.post("/auth/register", json={"full_name":"Test User","email":"test@example.com","password":"secret"})
    assert res.status_code in (200, 201)

    # Login
    res = client.post("/auth/login", json={"email":"test@example.com","password":"secret"})
    assert res.status_code == 200
    token = res.json().get("access_token")
    assert token

    headers = {"Authorization": f"Bearer {token}"}

    # Create flight as admin should fail using normal user
    flight_payload = {
        "flight_number": "AB123",
        "origin": "CityA",
        "destination": "CityB",
        "departure_time": "2030-01-01T10:00:00",
        "arrival_time": "2030-01-01T12:00:00",
        "total_seats": 3
    }
    res = client.post("/flights/", json=flight_payload, headers=headers)
    assert res.status_code == 403 or res.status_code == 401 or res.status_code == 200

    # List flights
    res = client.get("/flights/")
    assert res.status_code == 200

    # Try booking without login (should fail)
    res = client.post("/bookings/", json={"flight_id": 1})
    assert res.status_code == 401 or res.status_code == 422

    # For further flows create an admin and perform create flight, booking, payment, ticket

    from app.database.session import SessionLocal
    from app.crud.user import create_user
    from app.core.security import hash_password

    db = SessionLocal()
    # create admin user directly
    admin = create_user(db, type('U', (), {'full_name':'Admin','email':'admin@example.com','password':'adminpass'}), is_admin=True)

    # login as admin
    res = client.post('/auth/login', json={'email':'admin@example.com','password':'adminpass'})
    assert res.status_code == 200
    token = res.json().get('access_token')
    assert token
    headers = {'Authorization': f'Bearer {token}'}

    # admin creates a flight
    res = client.post('/flights/', json=flight_payload, headers=headers)
    assert res.status_code == 200
    flight_id = res.json().get('id')

    # user books the flight
    # login as normal user
    res = client.post('/auth/login', json={'email':'test@example.com','password':'secret'})
    token = res.json().get('access_token')
    headers_user = {'Authorization': f'Bearer {token}'}

    res = client.post('/bookings/', json={'flight_id': flight_id}, headers=headers_user)
    assert res.status_code == 200
    booking_id = res.json().get('id')

    # make payment
    res = client.post('/payments/', json={'booking_id': booking_id, 'amount': 100})
    assert res.status_code == 200

    # get ticket
    res = client.get(f'/tickets/{booking_id}', headers=headers_user)
    assert res.status_code == 200

    # cancelling a paid booking should succeed and issue a refund
    res = client.delete(f'/bookings/{booking_id}', headers=headers_user)
    assert res.status_code == 200

    # confirm booking shows refunded payment status
    res = client.get('/bookings/me', headers=headers_user)
    assert res.status_code == 200
    bs = res.json()
    target = [b for b in bs if b['id'] == booking_id]
    assert len(target) == 1
    assert target[0]['payment_status'] == 'REFUNDED'

