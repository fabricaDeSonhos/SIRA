from src.config import *
from src.service.reservation_service import *
from src.service.common_service import *

# generic object creation: auxiliar function
def create_simple_object(mclass, data):
    try:
        myjson = {"result": "ok"}               # prepare some default answer
        user = create_object(mclass, **data)    # try to create the object
        response = serialize_model(user)        # prepare an answer with the serialized object
        myjson.update({"details": response})    # add the serialized object to the answer
        return myjson                           # return the answer
    except Exception as ex:
        return {"result":"error", "details":f"error during object creation: {ex}"}

# --- POST's (creation) ---

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json                         # get the data
    answer = create_simple_object(User, data)   # try to create the object
    if answer["result"] == "ok":                # check the answer
        return jsonify(answer), 201             # Created :-)
    else:
        return jsonify(answer), 500             # Internal Server Error :-(

@app.route('/rooms', methods=['POST'])
def create_room():
    data = request.json                                                 # get the data
    answer = create_simple_object(Room, data)                           # create the object
    return jsonify(answer), 201 if answer["result"] == "ok" else 500    # return ok or error

@app.route('/reservations', methods=['POST'])
def create_reservation_route():
    try:
        myjson = {"result": "ok"}                        # prepare a "good" default answer :-)
        data = request.json                              # get request data
        room = get_object_by_id(Room, data['room_id'])   # get the room object
        user = get_object_by_id(User, data['user_id'])   # get the user object
        if not room or not user:                         # if room or user does not exists... error!
            return jsonify({"result": "error", "details": f"Invalid room_id ({room}) or user_id ({user})"}), 500    # error :-(
        else:
            # try to create the reservation; all fields are performed except room_id and user_id (already are in)
            res = create_reservation(room, user, **{k: v for k, v in data.items() if k not in ['room_id', 'user_id']})
            return jsonify(serialize_model(res)), 201      # happy return in this case :-)
    except Exception as ex:
        return jsonify({"result": "error", "details": f"error during reservation creation: {ex}"}), 500





# --- GET's LIST ---

# auxiliar function
def get_objects(mclass):
    try:
        myjson = {"result": "ok"}   
        objs = get_all_objects(mclass)                   # get all objects
        response = [serialize_model(u) for u in objs]  # serialize the objects
        myjson.update({"details": response})            # add the serialized object to the answer
        return myjson
    except Exception as ex:
        return {"result": "error", "details": f"error during {mclass} listing: {ex}"}

@app.route('/users', methods=['GET'])
def list_users():
    myjson = get_objects(User)
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 500

@app.route('/rooms', methods=['GET'])
def list_rooms():
    myjson = get_objects(Room)
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 500

@app.route('/reservations', methods=['GET'])
def list_reservations():
    myjson = get_objects(Reservation)
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 500



# --- GET's SPECIFIC ---

def get_specific_object(mclass, obj_id):
    try:
        myjson = {"result": "ok"}                       # prepare a "good" default answer :-)   
        obj = get_object_by_id(mclass, obj_id)           # get the object by id    
        if not obj:                                    # if user does not exists...  
            return jsonify({"result": "error", "details": f"{mclass}({obj_id}) not found "}), 404    # object not found
        response = serialize_model(object)                # serialize the user
        myjson.update({"details": response})            # add the serialized object to the answer   
        return myjson
    except Exception as ex:
        return {"result": "error", "details": f"error during specific object ({mclass}) retrieval: {ex}"}

@app.route('/users/<int:obj_id>', methods=['GET'])
def get_user(obj_id):
    myjson = get_object_by_id(User, obj_id)  
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 404

@app.route('/rooms/<int:obj_id>', methods=['GET'])
def get_room(obj_id):
    myjson = get_object_by_id(Room, obj_id)  
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 404

@app.route('/reservations/<uuid:obj_id>', methods=['GET'])
def get_room(obj_id):
    myjson = get_object_by_id(Reservation, obj_id)
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 404


# --- PUT's (UPDATE) ---

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = get_object_by_id(User, user_id)
    if not user:
        abort(404)
    for key, value in request.json.items():
        setattr(user, key, value)
    db.session.commit()
    return jsonify(serialize_model(user))

@app.route('/rooms/<int:room_id>', methods=['PUT'])
def update_room(room_id):
    room = get_object_by_id(Room, room_id)
    if not room:
        abort(404)
    for key, value in request.json.items():
        setattr(room, key, value)
    db.session.commit()
    return jsonify(serialize_model(room))


@app.route('/reservations/<uuid:res_id>', methods=['PUT'])
def update_reservation(res_id):
    reservation = get_object_by_id(Reservation, res_id)
    if not reservation:
        abort(404)
    for key, value in request.json.items():
        setattr(reservation, key, value)
    db.session.commit()
    return jsonify(serialize_model(reservation))

# --- DELETE's ---

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = get_object_by_id(User, user_id)
    if not user:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    return '', 204

@app.route('/rooms/<int:room_id>', methods=['DELETE'])
def delete_room(room_id):
    room = get_object_by_id(Room, room_id)
    if not room:
        abort(404)
    db.session.delete(room)
    db.session.commit()
    return '', 204

@app.route('/reservations/<uuid:res_id>', methods=['DELETE'])
def delete_reservation(res_id):
    reservation = get_object_by_id(Reservation, res_id)
    if not reservation:
        abort(404)
    db.session.delete(reservation)
    db.session.commit()
    return '', 204



# Only run if directly executed
if __name__ == '__main__':
    app.run(debug=True)

print("Routes loaded successfully.")