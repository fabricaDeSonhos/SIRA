from src.config import *
from src.model.user import *
from src.model.room import *

# https://stackoverflow.com/questions/73837260/using-kwargs-with-filter-by-sqlalchemy
# https://medium.com/@nadiaaoliverr/o-que-significa-args-e-kwargs-em-python-d18a4120b744

def create_object(m_class, **kwargs):
    obj = m_class(**kwargs)
    db.session.add(obj)
    db.session.commit()
    return obj

def get_object_by_id(m_class, object_id):
    return db.session.query(m_class).filter(m_class.id == object_id).first()

def get_objects(m_class):
    return db.session.query(m_class).all()
        
def get_object_by_name(m_class, name):
    obj = db.session.query(m_class).filter(m_class.name == name).first()
    return obj

def hard_delete_object_by_id(m_class, object_id):
    try:
        obj = db.session.query(m_class).filter(m_class.id == object_id).first()
        db.session.delete(obj)
        db.session.commit()    
        return True    
    except:
        return False
    
def soft_delete_object_by_id(m_class, object_id):
    try:
        obj = db.session.query(m_class).filter(m_class.id == object_id).first()
        obj.active = False
        db.session.commit()    
        return True    
    except:
        return False

# delete by the object itself
def hard_delete_object(obj):
    try:
        db.session.delete(obj)
        db.session.commit()
        return True    
    except:
        return False
    
def soft_delete_object(obj):
    try:
        obj.active = False
        db.session.commit()
        return True    
    except:
        return False