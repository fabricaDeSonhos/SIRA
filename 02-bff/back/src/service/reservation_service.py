from src.config import *
from src.model.reservation import *
from src.model.room import *
from src.model.user import *
from src.service.common_service import *

# Only ACTIVE Reservations are considered, by default
# except get_reservation_by_id 

def create_reservation(room, user, **kwargs):
    obj = Reservation(room=room, user=user, **kwargs)
    db.session.add(obj)
    db.session.commit()
    return obj

def soft_delete_reservation_by_id(canceler_user, reservation_id):
    try:
        obj = db.session.query(Reservation).filter(Reservation.id == reservation_id).first()
        obj.active = False
        obj.canceler_user = canceler_user
        db.session.commit()
        return {"result": "ok", "details": "Reservation canceled"}
    except Exception as ex:
        print(f"Error during soft delete of reservation by id: {ex}")
        return {"result": "error", "details": str(ex)}
    
def soft_delete_reservation(canceler_user, obj):
    try:
        obj.active = False
        obj.canceler_user = canceler_user
        db.session.commit()
        return {"result": "ok", "details": "Reservation canceled"}
    except Exception as ex:
        print(f"Error during soft delete of reservation: {ex}")
        return {"result": "error", "details": str(ex)}

def get_reservations():
    return db.session.query(Reservation).filter(Reservation.active == True).all()