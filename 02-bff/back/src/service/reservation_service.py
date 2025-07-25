from src.config import *
from src.model.reservation import *
from src.model.room import *
from src.model.user import *
from src.service.common_service import *

def create_reservation(room, user, **kwargs):
    obj = Reservation(room=room, user=user, **kwargs)
    db.session.add(obj)
    db.session.commit()
    return obj
