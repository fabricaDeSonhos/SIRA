from config import *
from model.reservation import *
from model.room import *
from model.user import *
from service.common_service import *

def create_reservation(room, user, **kwargs):
    obj = Reservation(room=room, user=user, **kwargs)
    db.session.add(obj)
    db.session.commit()
    return obj
