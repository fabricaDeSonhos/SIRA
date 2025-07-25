import pytest

from src.config import *
from src.service.common_service import *
from src.service.reservation_service import *

def test_creation():
    with app.app_context():

        # Create a new object
        room = create_object(Room, name="Lab A04")
        user = create_object(User, name="John Silva", 
                            email="jo@gmail.com", password="123")
        obj = create_reservation(room, user, purpose="Matemática 201 info")   

        assert obj.id is not None
        assert isinstance(obj.id, UUID)
        assert obj.purpose == "Matemática 201 info"
        assert obj.active is True

#def test_obj_delete():
#    with app.app_context():
 
        # testing delete method
        uuid = obj.id
        obj = get_object_by_id(Reservation, uuid)
        assert obj.purpose == "Matemática 201 info"
        ok = delete_object(obj)
        assert ok == True