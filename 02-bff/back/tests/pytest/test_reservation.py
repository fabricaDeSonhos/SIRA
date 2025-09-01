from tracemalloc import start
from datetime import date, datetime
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
        start_time = "10:00:00"
        end_time = "11:00:00"
        date_r = "2023-10-10"

        date_obj = datetime.strptime(date_r, "%Y-%m-%d").date()
        start_time_obj = datetime.strptime(start_time, "%H:%M:%S").time()
        end_time_obj = datetime.strptime(end_time, "%H:%M:%S").time()

        result = create_reservation(room, user, purpose="Matemática 201 info", start_time =start_time_obj, end_time=end_time_obj, date=date_obj)
        obj = result['details']
        
        assert obj.id is not None
        #assert isinstance(obj.id, UUID) # we are using Integer now
        assert isinstance(obj.id, int)
        assert obj.purpose == "Matemática 201 info"
        assert obj.active is True
        assert obj.room_id == room.id
        assert obj.user_id == user.id

        # create a conflicting reservation
        result2 = create_reservation(room, user, purpose="Matemática 201 info", start_time =start_time_obj, end_time=end_time_obj, date=date_obj)
        obj2 = result2['details']
        assert result2['result'] == "error"
        
        #with pytest.raises(Exception) as e_info:
        #    obj = create_reservation(room, user, purpose="Matemática 201 info")
        #assert str(e_info.value) == "Room already reserved for this time slot"
        

        # testing delete method
        id = obj.id
        obj = get_object_by_id(Reservation, id)
        assert obj.purpose == "Matemática 201 info"
        answer = soft_delete_reservation(user, obj)
        assert answer['result'] == "ok"