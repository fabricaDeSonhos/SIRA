import pytest

from src.config import *
from src.service.common_service import *

def test_creation():
    with app.app_context():
        obj = create_object(User, 
            name="Jack Johnson", 
            email="jack@gmail.com", 
            password="123")
        
        assert obj.id is not None
        assert isinstance(obj.id, int)
        assert obj.name == "Jack Johnson"
        assert obj.active is True

def test_obj_delete():
    with app.app_context():
        obj = get_object_by_name(User, "Jack Johnson")
        assert obj.name == "Jack Johnson"
        ok = delete_object(obj)
        assert ok == True