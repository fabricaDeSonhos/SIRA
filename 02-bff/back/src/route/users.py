
from src.config import *
from src.service.reservation_service import *
from src.service.common_service import *
from src.model.user import *
from src.model.reservation import *
from src.model.room import *

from src.route.routes import *

'''
curl http://localhost:5000/users -X POST -H 'content-type: application/json' -H 'Authorization: bearer
-d '{"name": "jorge", "password": "1234", "email": "jorge@yahoo.com", "admin": false, "active": true}'
'''
@app.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    data = request.json                         # get the data
    answer = create_simple_object(User, data)   # try to create the object
    return jsonify(answer), 201 if answer["result"] == "ok" else 500 # return created or internal error

@app.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    myjson = get_objects_helper(User)
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 500

@app.route('/user', methods=['GET'])
@jwt_required()
def get_authenticated_user():
    user_id = get_jwt_identity()
    myjson = get_specific_object(User, user_id)  
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 404

@app.route('/users/<int:obj_id>', methods=['GET'])
@jwt_required()
def get_user(obj_id):
    myjson = get_specific_object(User, obj_id)  
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 404

@app.route('/users/<int:obj_id>', methods=['PUT'])
@jwt_required()
def update_user(obj_id):
    myjson = update_object(User, obj_id)
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 500

@app.route('/users/<int:obj_id>', methods=['DELETE'])
@jwt_required()
def delete_user(obj_id):
    myjson = soft_delete_object(User, obj_id)
    return jsonify(myjson), 204 if myjson['result'] == 'ok' else 500
