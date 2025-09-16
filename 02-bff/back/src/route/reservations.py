
from src.config import *
from src.service.reservation_service import *
from src.service.common_service import *
from src.model.user import *
from src.model.reservation import *
from src.model.room import *

from src.route.routes import *
'''
curl -X POST http://localhost:5000/reservations \
  -H "Content-Type: application/json" \
  -d '{
    "room_id": 1,
    "user_id": 1,
    "date": "2023-10-10",
    "start_time": "10:00:00",
    "end_time": "11:00:00",
    "purpose": "Matemática 201 info"
  }'
'''

@app.route('/reservations', methods=['POST'])
@jwt_required()
def create_reservation_route():
    try:
        user_id = get_jwt_identity()
        data = request.json                              # get request data
        room = get_object_by_id(Room, data['room_id'])   # get the room object
        user = get_object_by_id(User, user_id)   # get the user object
        if not room:                         # if room or user does not exists... error!
            return jsonify({"result": "error", "details": f"Invalid room_id ({room})"}), 500    # error :-(
        else:
            # data conversion: convert date and time strings to date and time objects
            if 'date' in data and isinstance(data['date'], str):
                data['date'] = datetime.strptime(data['date'], "%Y-%m-%d").date()
            if 'start_time' in data and isinstance(data['start_time'], str):
                data['start_time'] = datetime.strptime(data['start_time'], "%H:%M:%S").time()
            if 'end_time' in data and isinstance(data['end_time'], str):
                data['end_time'] = datetime.strptime(data['end_time'], "%H:%M:%S").time()

            # try to create the reservation; all fields are performed except room_id and user_id (already are in)
            response = create_reservation(room, user, **{k: v for k, v in data.items() if k not in ['room_id', 'user_id']})
            
            # error?
            if response.get("result") == "error":  # error during reservation creation (probably conflict)
                return jsonify(response), 409
            
            object_json = response.get("details")

            return jsonify({"result":"ok", "details":object_json}), 201      # happy return in this case :-)
    except Exception as ex:
        return jsonify({"result": "error", "details": f"error during reservation creation: {ex}"}), 500

@app.route('/reservations', methods=['GET'])
#@jwt_required()
def list_reservations():
    myjson = get_reservations_helper()
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 500

# @app.route('/reservations/<uuid:obj_id>', methods=['GET'])
@app.route('/reservations/<int:obj_id>', methods=['GET'])
@jwt_required()
def get_reservation(obj_id):
    myjson = get_specific_object(Reservation, obj_id)
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 404


# @app.route('/reservations/<uuid:obj_id>', methods=['PUT'])
@app.route('/reservations/<int:obj_id>', methods=['PUT'])
@jwt_required()
def update_reservation(obj_id):
    myjson = update_object(Reservation, obj_id)
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 500

# @app.route('/reservations/<uuid:obj_id>/<int:canceler_user_id>', methods=['DELETE'])
@app.route('/reservations/<int:obj_id>', methods=['DELETE'])
@jwt_required()
def delete_reservation(obj_id):
    try:
        canceler_user_id = get_jwt_identity()
        canceler_user = get_object_by_id(User, canceler_user_id) # get the user who is canceling this reservation
        if not canceler_user:
            print(f"Invalid canceler_user_id: {canceler_user_id}")
            return jsonify({"result": "error", "details": f"Invalid canceler_user_id ({canceler_user_id})"}), 500    # error :-(
        myjson = soft_delete_reservation_by_id(canceler_user=canceler_user, reservation_id=obj_id)
        return jsonify(myjson), 204 if myjson['result'] == 'ok' else 500
    except Exception as ex:
        print(f"Error during reservation deletion: {ex}")
        return jsonify({"result": "error", "details": f"error during canceler_user retrieval: {ex}"}), 500
