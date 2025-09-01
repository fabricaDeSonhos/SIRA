# from src.config import app, db (não sei porque esse não funciona)
from email.header import Header
from src.route.routes import app, db
from datetime import date, time

import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_user_crud(client):

    headers = {"Content-Type": "application/json"}

    # obtain a TOKEN
    res = client.post('/login', data={"email": "admin", "password": "admin"},
                        headers=headers)
    
    assert res.status_code == 200
    json = res.get_json()
    assert json["result"] == "ok"
    assert "token" in json["details"]   

    token = json["details"]["token"]

    # GET ALL
    res = client.get(f"/users", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    json = res.get_json()
    assert json["result"] == "ok"
    assert isinstance(json["details"], list)
    print(f"Users found: {len(json['details'])}")
    
    # POST
    headers = {"Content-Type": "application/json"}
    res = client.post('/users', 
                      headers=headers, 
                      json={"name": "Alice", "email": "alice@example.com", "password": "pass"})
    print(res.status_code)
    print(res.get_json())
    assert res.status_code == 201
        
    # get the field "id" from "details" content
    json = res.get_json()
    assert json["result"] == "ok"
    assert "id" in json["details"]
    person = json["details"]
    user_id = person["id"]
    assert user_id is not None
    assert isinstance(user_id, int)
    assert person["password"] == "pass"
    print(f"User created with ID: {user_id}")
    print(f"details: {person}")
    # print(f"id: {json["details"]["id"]}")
    
    
    # GET SPECIFIC
    res = client.get(f"/users/{user_id}")
    # print(f"get specific: {res}")
    json = res.get_json()
    print(f"id: {json["details"]["id"]}")
    assert res.status_code == 200
    assert json["result"] == "ok"
    assert json["details"]["id"] == user_id

    # PUT (update)
    res = client.put(f"/users/{user_id}", json={"name": "Alice Smith Silva"})
    assert res.status_code == 200
    json = res.get_json()
    assert json["details"]["name"] == "Alice Smith Silva"

    # DELETE
    res = client.delete(f"/users/{user_id}")
    assert res.status_code == 204

def test_room_crud(client):
    res = client.post('/rooms', json={"name": "Room A"})
    assert res.status_code == 201
    room_id = res.get_json()["details"]["id"]

    res = client.get(f"/rooms/{room_id}")
    assert res.status_code == 200

    res = client.put(f"/rooms/{room_id}", json={"name": "Updated Room"})
    assert res.status_code == 200
    assert res.get_json()["details"]["name"] == "Updated Room"

    res = client.delete(f"/rooms/{room_id}")
    assert res.status_code == 204

def test_reservation_crud(client):
    
    # Create user
    r1 = client.post('/users', json={"name": "Bob", "email": "bob@example.com", "password": "pass"}).get_json()
    assert r1 is not None
    assert "result" in r1
    assert "details" in r1
    assert r1["details"] is not None
    assert r1["result"] is not None
    assert r1["result"] == "ok"
    
    user = r1["details"]
    assert "id" in user
    
    # Create room
    r2 = client.post('/rooms', json={"name": "Room B"}).get_json()
    if r2["result"] != "ok":
        pytest.fail(f"Failed to create room: {r2['details']}")
    
    room = r2["details"]

    # Create reservation
    res = client.post('/reservations', json={
        "room_id": room["id"],
        "user_id": user["id"],
        "purpose": "Team Meeting",
        "date": "2023-10-10",
        "start_time": "10:00:00",
        "end_time": "11:00:00"
    })

    assert res.status_code == 201
    answer = res.get_json()
    assert answer["result"] == "ok"
    reservation = answer["details"]
    assert "id" in reservation
    reservation_id = reservation["id"]
    #reservation_id = answer["details"]["id"]

    res = client.get(f"/reservations/{reservation_id}")
    assert res.status_code == 200

    res = client.put(f"/reservations/{reservation_id}", json={"purpose": "Updated Meeting"})
    assert res.status_code == 200
    assert res.get_json()["details"]["purpose"] == "Updated Meeting"

    res = client.delete(f"/reservations/{reservation_id}/{user['id']}")
    assert res.status_code == 204