from src.config import *
from src.model.reservation import *
from src.model.room import *
from src.model.user import *
from src.service.common_service import *

# Only ACTIVE Reservations are considered, by default
# except get_reservation_by_id 

def get_conflicting_reservations(room_id, start_time, end_time):
    if start_time is None or end_time is None:
        # precisa de melhor tratamento de erros aqui
        raise ValueError("start_time and end_time must not be None")

    existing_reservations = db.session.query(Reservation).filter(
        Reservation.room_id == room_id,
        Reservation.active.is_(True),
        Reservation.start_time < end_time,
        Reservation.end_time > start_time
    ).all()
    
    # conflits?
    if existing_reservations:
        ids = [res.id for res in existing_reservations]
        # return IDs of conflicting reservations
        return ids
    
    # no conflits    
    return []

def create_reservation(room, user, **kwargs):
    # check if there is another reservation that could conflict
    existing_reservations = get_conflicting_reservations(
        room_id=room.id,
        start_time=kwargs.get('start_time'),
        end_time=kwargs.get('end_time'))
    
    # conflict found?
    if existing_reservations:
        # answer with error
        return {"result": "error", "details": "Existem reservas conflitantes para este período: " + str(ids)}
    
    obj = Reservation(room=room, user=user, **kwargs)
    db.session.add(obj)
    db.session.commit()
    return {"result": "ok", "details": "Existem reservas conflitantes para este período: " + str(ids)}
    
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