# from src.config import app, db (não sei porque esse não funciona)
from email.header import Header

from requests import head
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

def get_token(client):
    headers = {"Content-Type": "application/json"}
    res = client.post('/login', 
                      json={"email": "admin", "password": "admin"},
                      headers=headers)
    assert res.status_code == 200
    json = res.get_json()
    assert json["result"] == "ok"
    assert "token" in json["details"]   
    token = json["details"]["token"]
    return token

def test_user_crud(client):

    token = get_token(client)
    assert token is not None
    assert isinstance(token, str) 

    # headers of an authenticated request
    headers = {"Content-Type": "application/json",
                "Authorization": f"Bearer {token}"}
   

    # get all users
    res = client.get(f"/users", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    json = res.get_json()
    assert json["result"] == "ok"
    assert isinstance(json["details"], list)
    print(f"Users found: {len(json['details'])}")
    
    # POST
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
    res = client.get(f"/users/{user_id}", headers=headers)
    # print(f"get specific: {res}")
    json = res.get_json()
    print(f"get specific: {json}")
    print(f"id: {json["details"]["id"]}")
    assert res.status_code == 200
    assert json["result"] == "ok"
    assert json["details"]["id"] == user_id

    # PUT (update)
    res = client.put(f"/users/{user_id}", 
                     json={"name": "Alice Smith Silva"},
                     headers=headers)
    assert res.status_code == 200
    json = res.get_json()
    assert json["details"]["name"] == "Alice Smith Silva"

    # DELETE
    res = client.delete(f"/users/{user_id}",
                        headers=headers)
    assert res.status_code == 204

def test_room_crud(client):

    token = get_token(client)
    assert token is not None
    assert isinstance(token, str) 

    # headers of an authenticated request
    headers = {"Content-Type": "application/json",
                "Authorization": f"Bearer {token}"}

    res = client.post('/rooms', 
                      json={"name": "Room A"},
                      headers=headers)
    
    assert res.status_code == 201
    room_id = res.get_json()["details"]["id"]

    res = client.get(f"/rooms/{room_id}", 
                     headers=headers)
    assert res.status_code == 200

    res = client.put(f"/rooms/{room_id}", 
                     json={"name": "Updated Room"},
                     headers=headers)
    assert res.status_code == 200
    assert res.get_json()["details"]["name"] == "Updated Room"

    res = client.delete(f"/rooms/{room_id}",
                        headers=headers)
    assert res.status_code == 204

def test_reservation_crud(client):
    
    token = get_token(client)
    assert token is not None
    assert isinstance(token, str) 

    # headers of an authenticated request
    headers = {"Content-Type": "application/json",
                "Authorization": f"Bearer {token}"}

    # Create user
    response = client.post('/users', 
                     json={"name": "Bob", "email": "bob@example.com", "password": "pass"},
                     headers=headers)
    r1 = response.get_json()
    assert r1 is not None
    assert "result" in r1
    assert "details" in r1
    assert r1["details"] is not None
    assert r1["result"] is not None
    assert r1["result"] == "ok"
    
    user = r1["details"]
    assert "id" in user
    
    # Create room
    response = client.post('/rooms', 
                           json={"name": "Room B"}, 
                           headers=headers)
    r2 = response.get_json()
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
    },
    headers=headers)

    assert res.status_code == 201
    answer = res.get_json()
    assert answer["result"] == "ok"
    reservation = answer["details"]
    assert "id" in reservation
    reservation_id = reservation["id"]
    #reservation_id = answer["details"]["id"]

    print(f"Created reservation with ID: {reservation_id}")
    res = client.get(f"/reservations/{reservation_id}", 
                     headers=headers)
    
    assert res.status_code == 200

    res = client.put(f"/reservations/{reservation_id}", 
                     json={"purpose": "Updated Meeting"},
                     headers=headers)
    assert res.status_code == 200
    assert res.get_json()["details"]["purpose"] == "Updated Meeting"

    res = client.delete(f"/reservations/{reservation_id}/{user['id']}",
                        headers=headers)
    assert res.status_code == 204