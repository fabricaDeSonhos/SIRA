
from src.config import *
from src.service.reservation_service import *
from src.service.common_service import *
from src.model.user import *
from src.model.reservation import *
from src.model.room import *

from src.route.routes import *

@app.route('/rooms', methods=['POST'])
@jwt_required()
def create_room():
    data = request.json                                                 # get the data
    answer = create_simple_object(Room, data)                           # create the object
    return jsonify(answer), 201 if answer["result"] == "ok" else 500    # return ok or error

@app.route('/rooms', methods=['GET'])
#@jwt_required()
def list_rooms():
    myjson = get_objects_helper(Room)
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 500

@app.route('/rooms/labs', methods=['GET'])
#@jwt_required()
def list_labs():
    my_json = ""
    try:
        myjson = {"result": "ok"}   
        objs = db.session.query(Room).filter(Room.type == "Laboratório de Informática", Room.active == True).all()
        response = [serialize_model(u) for u in objs]  # serialize the objects
        myjson.update({"details": response})            # add the serialized object to the answer
    except Exception as ex:
        print(f"Error during info labs listing: {ex}")
        myjson = {"result": "error", "details": f"error during info labsl isting: {ex}"}
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 500

@app.route('/rooms/<int:obj_id>', methods=['GET'])
@jwt_required()
def get_room(obj_id):
    myjson = get_specific_object(Room, obj_id)  
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 404

@app.route('/rooms/<int:obj_id>', methods=['PUT'])
@jwt_required()
def update_room(obj_id):
    myjson = update_object(Room, obj_id)
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 500

@app.route('/rooms/<int:obj_id>', methods=['DELETE'])
@jwt_required()
def delete_room(obj_id):
    myjson = soft_delete_object(Room, obj_id)
    return jsonify(myjson), 204 if myjson['result'] == 'ok' else 500
