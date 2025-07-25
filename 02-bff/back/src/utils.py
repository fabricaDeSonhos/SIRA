from datetime import datetime
def current_time():
    return datetime.now().time()

def serialize_model(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}