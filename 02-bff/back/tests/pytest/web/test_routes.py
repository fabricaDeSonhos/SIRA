#from src.config import *
from src.route.routes import app, db, User, Room, Reservation
# Remove or comment out: from src.config import *
#from app import app, db, User, Room, Reservation
#from uuid import uuid4
from datetime import date, time

import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_user_crud(client):
    headers = {"Content-Type": "application/json"}
    res = client.post('/users', 
                      headers=headers, 
                      json={"name": "Alice", "email": "alice@example.com", "password": "pass"})
    assert res.status_code == 201
    
    # field "id" from "details" content
    user_id = res.get_json()["details"]["id"]

    res = client.get(f"/users/{user_id}")
    assert res.status_code == 200

    res = client.put(f"/users/{user_id}", json={"name": "Alice Smith"})
    assert res.status_code == 200
    assert res.get_json()["name"] == "Alice Smith"

    res = client.delete(f"/users/{user_id}")
    assert res.status_code == 204

def test_room_crud(client):
    res = client.post('/rooms', json={"name": "Room A"})
    assert res.status_code == 201
    room_id = res.get_json()["id"]

    res = client.get(f"/rooms/{room_id}")
    assert res.status_code == 200

    res = client.put(f"/rooms/{room_id}", json={"name": "Updated Room"})
    assert res.status_code == 200
    assert res.get_json()["name"] == "Updated Room"

    res = client.delete(f"/rooms/{room_id}")
    assert res.status_code == 204


def test_reservation_crud(client):
    # Create user and room first
    user = client.post('/users', json={"name": "Bob", "email": "bob@example.com", "password": "pass"}).get_json()
    room = client.post('/rooms', json={"name": "Room B"}).get_json()

    res = client.post('/reservations', json={
        "user_id": user["id"],
        "room_id": room["id"],
        "date": str(date.today()),
        "start_time": "10:00:00",
        "end_time": "11:00:00",
        "purpose": "Meeting"
    })
    assert res.status_code == 201
    reservation_id = res.get_json()["id"]

    res = client.get(f"/reservations/{reservation_id}")
    assert res.status_code == 200

    res = client.put(f"/reservations/{reservation_id}", json={"purpose": "Updated Meeting"})
    assert res.status_code == 200
    assert res.get_json()["purpose"] == "Updated Meeting"

    res = client.delete(f"/reservations/{reservation_id}")
    assert res.status_code == 204

