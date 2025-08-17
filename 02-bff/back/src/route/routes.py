from src.config import *
from src.service.reservation_service import *
from src.service.common_service import *
from src.model.user import *
from src.model.reservation import *
from src.model.room import *

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

jwt = JWTManager(app)

# --- security: LOGIN
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json  # get the data
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({"result": "error", "details": "Invalid login data"}), 400  # bad request

        email = data['email']
        # BY NOW, the username that is coming from the front is the email
        user = get_user_by_email(email)  
        if not user or not user.check_password(data['password']):  # check password
            return jsonify({"result": "error", "details": "Invalid email or password"}), 401  # unauthorized

        token = create_access_token(identity=email)
        response = serialize_model(user)  # serialize the user object
        response.update({"token": token})  # add the token to the response
        return jsonify({"result": "ok", "details": response}), 200  # ok response
    except Exception as ex:
        return jsonify({"result": "error", "details": f"Error during login: {ex}"}), 500

# --- security: LOGOUT
# NOT IMPLEMENTED YET
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        jti = get_jwt_identity()  # get the JWT identity (email)
        # Here you would typically add the jti to a blacklist or similar mechanism
        return jsonify({"result": "ok", "details": "Logged out successfully"}), 200  # ok response
    except Exception as ex:
        return jsonify({"result": "error", "details": f"Error during logout: {ex}"}), 500
    
# --- POST's (creation) ---

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

@app.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    data = request.json                         # get the data
    answer = create_simple_object(User, data)   # try to create the object
    return jsonify(answer), 201 if answer["result"] == "ok" else 500 # return created or internal error

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
            # data conversion: convert date and time strings to date and time objects
            if 'date' in data and isinstance(data['date'], str):
                data['date'] = datetime.strptime(data['date'], "%Y-%m-%d").date()
            if 'start_time' in data and isinstance(data['start_time'], str):
                data['start_time'] = datetime.strptime(data['start_time'], "%H:%M:%S").time()
            if 'end_time' in data and isinstance(data['end_time'], str):
                data['end_time'] = datetime.strptime(data['end_time'], "%H:%M:%S").time()

            print("ok 1")
            # try to create the reservation; all fields are performed except room_id and user_id (already are in)
            res = create_reservation(room, user, **{k: v for k, v in data.items() if k not in ['room_id', 'user_id']})
            print("ok 2")
            response = serialize_model(res)             # serialize the reservation object
            print("ok 3")
            myjson.update({"details": response})        # add the serialized object to the answer
            return jsonify(myjson), 201      # happy return in this case :-)
    except Exception as ex:
        print(ex)
        return jsonify({"result": "error", "details": f"error during reservation creation: {ex}"}), 500





# --- GET's LIST ---

# auxiliar function
def get_objects_helper(mclass):
    try:
        myjson = {"result": "ok"}   
        objs = get_objects(mclass)                   # get all objects
        response = [serialize_model(u) for u in objs]  # serialize the objects
        myjson.update({"details": response})            # add the serialized object to the answer
        return myjson
    except Exception as ex:
        print(f"Error during {mclass} listing: {ex}")
        return {"result": "error", "details": f"error during {mclass} listing: {ex}"}

def get_reservations_helper():
    try:
        myjson = {"result": "ok"}   
        objs = get_reservations()                   # get all objects
        response = [serialize_model(u) for u in objs]  # serialize the objects
        myjson.update({"details": response})            # add the serialized object to the answer
        return myjson
    except Exception as ex:
        print(f"Error during {mclass} listing: {ex}")
        return {"result": "error", "details": f"error during {mclass} listing: {ex}"}

@app.route('/users', methods=['GET'])
def list_users():
    myjson = get_objects_helper(User)
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 500

@app.route('/rooms', methods=['GET'])
def list_rooms():
    myjson = get_objects_helper(Room)
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 500

@app.route('/reservations', methods=['GET'])
def list_reservations():
    myjson = get_reservations_helper()
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 500



# --- GET's SPECIFIC ---

def get_specific_object(mclass, obj_id):
    try:
        myjson = {"result": "ok"}                       # prepare a "good" default answer :-)   
        obj = get_object_by_id(mclass, obj_id)           # get the object by id    
        if not obj:                                    # if user does not exists...  
            return jsonify({"result": "error", "details": f"{mclass}({obj_id}) not found "}), 404    # object not found
        response = serialize_model(obj)                # serialize the user
        myjson.update({"details": response})            # add the serialized object to the answer   
        print(myjson)
        return myjson
    except Exception as ex:
        return {"result": "error", "details": f"error during specific object ({mclass}) retrieval: {ex}"}

@app.route('/users/<int:obj_id>', methods=['GET'])
def get_user(obj_id):
    myjson = get_specific_object(User, obj_id)  
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 404

@app.route('/rooms/<int:obj_id>', methods=['GET'])
def get_room(obj_id):
    myjson = get_specific_object(Room, obj_id)  
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 404

@app.route('/reservations/<uuid:obj_id>', methods=['GET'])
def get_reservation(obj_id):
    myjson = get_specific_object(Reservation, obj_id)
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 404

# --- PUT's (UPDATE) ---

def update_object(mclass, obj_id):
    try:
        myjson = {"result": "ok"}                       # prepare a "good" default answer :-)   
    
        obj = get_object_by_id(mclass, obj_id)
        if not obj:
            return {"result": "error", "details": f"{mclass}({obj_id}) not found "}
        for key, value in request.json.items():         # update the object
            setattr(obj, key, value)
        db.session.commit()                            # confirm the update
        response = serialize_model(obj)                # serialize the updated object
        myjson.update({"details": response})           # add the serialized object to the answer
        return myjson
    except Exception as ex:
        return {"result": "error", "details": f"error during object ({mclass}) update: {ex}"}

@app.route('/users/<int:obj_id>', methods=['PUT'])
def update_user(obj_id):
    myjson = update_object(User, obj_id)
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 500

@app.route('/rooms/<int:obj_id>', methods=['PUT'])
def update_room(obj_id):
    myjson = update_object(Room, obj_id)
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 500

@app.route('/reservations/<uuid:obj_id>', methods=['PUT'])
def update_reservation(obj_id):
    myjson = update_object(Reservation, obj_id)
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 500

# --- DELETE's ---

def hard_delete_object(mclass, obj_id):
    try:
        myjson = {"result": "ok"}                       # prepare a "good" default answer :-)   
    
        obj = get_object_by_id(mclass, obj_id)
        if not obj:
            return {"result": "error", "details": f"{mclass}({obj_id}) not found "}
        db.session.delete(obj)
        db.session.commit()
        myjson.update({"details": "ok"})
        return myjson
    except Exception as ex:
        print(f"Error during hard delete of object {mclass} with id {obj_id}: {ex}")
        return {"result": "error", "details": f"error during object ({mclass}) exclusion: {ex}"}

def soft_delete_object(mclass, obj_id):
    try:
        myjson = {"result": "ok"}                       # prepare a "good" default answer :-)   
    
        obj = get_object_by_id(mclass, obj_id)
        if not obj:
            return {"result": "error", "details": f"{mclass}({obj_id}) not found "}
        obj.active = False  # set the object as inactive
        db.session.commit()
        myjson.update({"details": "The Active property of the object was set to False"})
        return myjson
    except Exception as ex:
        print(f"Error during soft delete of object {mclass} with id {obj_id}: {ex}")
        return {"result": "error", "details": f"error during object ({mclass}) exclusion: {ex}"}

@app.route('/users/<int:obj_id>', methods=['DELETE'])
def delete_user(obj_id):
    myjson = soft_delete_object(User, obj_id)
    return jsonify(myjson), 204 if myjson['result'] == 'ok' else 500

@app.route('/rooms/<int:obj_id>', methods=['DELETE'])
def delete_room(obj_id):
    myjson = soft_delete_object(Room, obj_id)
    return jsonify(myjson), 204 if myjson['result'] == 'ok' else 500

@app.route('/reservations/<uuid:obj_id>/<int:canceler_user_id>', methods=['DELETE'])
def delete_reservation(obj_id, canceler_user_id):
    try:
        canceler_user = get_object_by_id(User, canceler_user_id) # get the user who is canceling this reservation
        if not canceler_user:
            print(f"Invalid canceler_user_id: {canceler_user_id}")
            return jsonify({"result": "error", "details": f"Invalid canceler_user_id ({canceler_user_id})"}), 500    # error :-(
        myjson = soft_delete_reservation_by_id(canceler_user=canceler_user, reservation_id=obj_id)
        return jsonify(myjson), 204 if myjson['result'] == 'ok' else 500
    except Exception as ex:
        print(f"Error during reservation deletion: {ex}")
        return jsonify({"result": "error", "details": f"error during canceler_user retrieval: {ex}"}), 500

# Only run if directly executed
if __name__ == '__main__':
    app.run() # debug=True)

print("Routes loaded successfully.")
