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
        assert obj.room_id == room.id
        assert obj.user_id == user.id

        # create a conflicting reservation
        obj = create_reservation(room, user, purpose="Matemática 201 info")
        assert str(obj['result']) == "Room already reserved for this time slot"
        #with pytest.raises(Exception) as e_info:
        #    obj = create_reservation(room, user, purpose="Matemática 201 info")
        #assert str(e_info.value) == "Room already reserved for this time slot"
        

        # testing delete method
        uuid = obj.id
        obj = get_object_by_id(Reservation, uuid)
        assert obj.purpose == "Matemática 201 info"
        answer = soft_delete_reservation(user, obj)
        assert answer['result'] == "ok"