#from src.config import *
from src.route.routes import app, db, User, Room, Reservation
# Remove or comment out: from src.config import *
#from app import app, db, User, Room, Reservation
#from uuid import uuid4
from datetime import date, time
import requests

def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_user_crud(client):
    headers = {"Content-Type": "application/json"}
    res = requests.post('http://localhost:5000/users', 
                      headers=headers, 
                      json={"name": "Alice", "email": "alice@example.com", "password": "pass"})
    print(res.status_code)
    print(res.json())
    
# start tests
cli = client()
test_user_crud(cli)