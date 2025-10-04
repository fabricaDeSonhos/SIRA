from src.config import *
from src.service.reservation_service import *
from src.service.common_service import *
from src.model.user import *
from src.model.reservation import *
from src.model.room import *

'''
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "jorge@yahoo.com", "password": "1234"}'
'''

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

        token = create_access_token(identity=str(user.id))
        response = serialize_model(user)  # serialize the user object
        response.update({"token": token})  # add the token to the response
        return jsonify({"result": "ok", "details": response}), 200  # ok response
    except Exception as ex:
        app.logger.debug(f"Error during login: {ex}"    )
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
        print(f"Error during Reservations listing: {ex}")
        return {"result": "error", "details": f"error during Reservations listing: {ex}"}






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




# --- PUT's (UPDATE) ---

def update_object(mclass, obj_id):
    try:
        myjson = {"result": "ok"}                       # prepare a "good" default answer :-)   
    
        obj = get_object_by_id(mclass, obj_id)
        if not obj:
            return {"result": "error", "details": f"{mclass}({obj_id}) not found "}
        for key, value in request.json.items():         # update the object
            if 'date' == key and isinstance(value, str):
                value = datetime.strptime(value, "%Y-%m-%d").date()
            if 'start_time' == key and isinstance(value, str):
                value = datetime.strptime(value, "%H:%M:%S").time()
            if 'end_time' == key and isinstance(value, str):
                value = datetime.strptime(value, "%H:%M:%S").time()
            setattr(obj, key, value)
        db.session.commit()                            # confirm the update
        response = serialize_model(obj)                # serialize the updated object
        myjson.update({"details": response})           # add the serialized object to the answer
        return myjson
    except Exception as ex:
        return {"result": "error", "details": f"error during object ({mclass}) update: {ex}"}



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



# Only run if directly executed
if __name__ == '__main__':
    app.run() # debug=True)

print("Routes loaded successfully.")
