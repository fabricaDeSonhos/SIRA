from datetime import datetime, date, time

def current_time():
    return datetime.now().time()

def serialize_model(obj):
    # return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
    result = {}
    for column in obj.__table__.columns:
        value = getattr(obj, column.name)
        result[column.name] = value
        try:
            if isinstance(value, (date, time, datetime)): # try to check is the value is an special value
                result[column.name] = value.isoformat()
        except Exception as e:
            print(f"Error getting isoformat from {column.name}: {e}")
    return result