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

from src.config import *
from src.service.common_service import *

def test_creation():
    with app.app_context():
        obj = create_object(Room, name="Conference Room", active=True)
        
        assert obj.id is not None
        #assert isinstance(room.id, UUID)
        assert isinstance(obj.id, int)
        assert obj.name == "Conference Room"
        assert obj.active is True

def test_obj_delete():
    with app.app_context():
        obj = get_object_by_name(Room, "Conference Room")
        assert obj.name == "Conference Room"
        ok = soft_delete_object(obj)
        assert ok == True