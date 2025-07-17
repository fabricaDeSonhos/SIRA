from config import *
from model.room import *

def create_room(name, active=True):
    room = Room(name=name, active=active)
    db.session.add(room)
    db.session.commit()
    return room

def get_room_by_id(room_id):
    room = db.session.query(Room).filter(Room.id == room_id).first()
    return room

def get_room_by_name(room_name):
    room = db.session.query(Room).filter(Room.name == room_name).first()
    return room

def get_all_rooms():
    return db.session.query(Room).all()

def delete_room_by_id(room_id):
    try:
        room = db.session.query(Room).filter(Room.id == room_id).first()
        db.session.delete(room)
        db.session.commit()
        return True    
    except:
        return False

# delete by the object itself
def delete_room(room):
    try:
        db.session.delete(room)
        db.session.commit()
        return True    
    except:
        return False