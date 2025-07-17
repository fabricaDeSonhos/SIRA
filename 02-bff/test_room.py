'''

https://flask-sqlalchemy.readthedocs.io/en/stable/contexts/#tests

When pytest is run, it will search all 
directories below where it was called, 
find all of the Python files in these 
directories whose names start or 
end with test , import them, 
and run all of the functions and 
classes whose names start with test or Test .

'''

import pytest

from config import *
#from model.room import *
from service.room_service import *

def test_room_creation():
    with app.app_context():
        room = create_room(name="Conference Room", active=True)
        
        assert room.id is not None
        #assert isinstance(room.id, UUID)
        assert isinstance(room.id, int)
        assert room.name == "Conference Room"
        assert room.active is True

def test_room_delete_first_room():
    with app.app_context():
        room = get_room_by_name("Conference Room")
        assert room.name == "Conference Room"
        ok = delete_room(room)
        assert ok == True
