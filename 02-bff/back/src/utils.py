from datetime import datetime
def current_time():
    return datetime.now().time()

def serialize_model(obj):
    # return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
    result = {}
    for column in obj.__table__.columns:
        value = getattr(obj, column.name)
        if isinstance(value, (datetime.date, datetime.time)):
            result[column.name] = value.isoformat()
        else:
            result[column.name] = value
    return result