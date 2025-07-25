from src.config import *
from src.service.reservation_service import *
from src.service.common_service import *

# generic object creation
def create_simple_object(mclass, data):
    try:
        #prepare some default answer
        myjson = {"result": "ok"}
        
        # try to create the object
        user = create_object(mclass, **data)
        # prepare an answer with the serialized object
        response = serialize_model(user)
        # add the answer to the response
        myjson.update({"details": response})
        # return the answer
        return myjson
    except Exception as ex:
        return {"result":"error", "details":f"error during object creation: {ex}"}

# ----- USERS -----
@app.route('/users', methods=['POST'])
def create_user():
    # get the data
    data = request.json
    #  try to create the object
    answer = create_simple_object(User, data)
    # check the answer
    if answer["result"] == "ok":
        return jsonify(answer), 201 # Created
    else:
        return jsonify(answer), 500 # Internal Server Error


@app.route('/users', methods=['GET'])
def list_users():
    users = get_all_objects(User)
    return jsonify([serialize_model(u) for u in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_object_by_id(User, user_id)
    if not user:
        abort(404)
    return jsonify(serialize_model(user))

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = get_object_by_id(User, user_id)
    if not user:
        abort(404)
    for key, value in request.json.items():
        setattr(user, key, value)
    db.session.commit()
    return jsonify(serialize_model(user))

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = get_object_by_id(User, user_id)
    if not user:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    return '', 204

# ----- ROOMS -----
@app.route('/rooms', methods=['POST'])
def create_room():
    data = request.json
    room = create_object(Room, **data)
    return jsonify(serialize_model(room)), 201

@app.route('/rooms', methods=['GET'])
def list_rooms():
    rooms = get_all_objects(Room)
    return jsonify([serialize_model(r) for r in rooms])

@app.route('/rooms/<int:room_id>', methods=['GET'])
def get_room(room_id):
    room = get_object_by_id(Room, room_id)
    if not room:
        abort(404)
    return jsonify(serialize_model(room))

@app.route('/rooms/<int:room_id>', methods=['PUT'])
def update_room(room_id):
    room = get_object_by_id(Room, room_id)
    if not room:
        abort(404)
    for key, value in request.json.items():
        setattr(room, key, value)
    db.session.commit()
    return jsonify(serialize_model(room))

@app.route('/rooms/<int:room_id>', methods=['DELETE'])
def delete_room(room_id):
    room = get_object_by_id(Room, room_id)
    if not room:
        abort(404)
    db.session.delete(room)
    db.session.commit()
    return '', 204

# ----- RESERVATIONS -----
@app.route('/reservations', methods=['POST'])
def create_reservation_route():
    data = request.json
    room = get_object_by_id(Room, data['room_id'])
    user = get_object_by_id(User, data['user_id'])
    if not room or not user:
        abort(400, description="Invalid room_id or user_id")
    res = create_reservation(room, user, **{k: v for k, v in data.items() if k not in ['room_id', 'user_id']})
    return jsonify(serialize_model(res)), 201

@app.route('/reservations', methods=['GET'])
def list_reservations():
    reservations = get_all_objects(Reservation)
    return jsonify([serialize_model(r) for r in reservations])

@app.route('/reservations/<uuid:res_id>', methods=['GET'])
def get_reservation(res_id):
    reservation = get_object_by_id(Reservation, res_id)
    if not reservation:
        abort(404)
    return jsonify(serialize_model(reservation))

@app.route('/reservations/<uuid:res_id>', methods=['PUT'])
def update_reservation(res_id):
    reservation = get_object_by_id(Reservation, res_id)
    if not reservation:
        abort(404)
    for key, value in request.json.items():
        setattr(reservation, key, value)
    db.session.commit()
    return jsonify(serialize_model(reservation))

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
