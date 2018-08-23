#!/usr/bin/python3
"""
    Handles RESTful API actions for User objects
"""


from models import BaseModel
from models import storage
from api.v1.views import app_views
from flask import jsonify
from flask import make_response
from flask import abort
from flask import request
from models import User


@app_views.route("/users")
def users():
    """
    prints all users
    """
    obj_list = []
    json_list = []
    json_users = storage.all("User")
    for user_obj in json_users.values():
        obj_list.append(user_obj)
    for user in obj_list:
        json_list.append(user.to_dict())
    return jsonify(json_list)


@app_views.route("/users/<user_id>", methods=['GET'])
def get_user(user_id):
    """
    gets a user
    """
    get_user = storage.get("User", user_id)
    if get_user is None:
        abort(404)
    return jsonify(get_user.to_dict()), 200


@app_views.route("/users/<user_id>", methods=['DELETE'])
def delete_user(user_id):
   """
   deletes a user
   """
   empty_dict = {}

   try:
       json_user = storage.get("User", user_id)
       json_user.delete()
       storage.save()
       return jsonify(empty_dict), 200
   except Exception:
       abort(404)


@app_views.route("/states", methods=['POST'])
def post_states():
   """
   posts a user
   """
    content = request.get_json()
    if content is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in content:
        return jsonify({"error": "Missing name"}), 400
    exclude = ['id', 'created_at', 'updated_at']
    for e in exclude:
        content.pop(e, None)
    new_state = State(**content)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 200

"""
@app_views.route("/states/<state_id>", methods=['PUT'])
def put_states(state_id):
   
    new_state = None
    obj_list = []
    content = request.get_json()
    if content is None:
        return jsonify({"error": "Not a JSON"}), 400
    exclude = ['id', 'created_at', 'updated_at']
    for e in exclude:
        content.pop(e, None)
    json_states = storage.all("State")
    for state_obj in json_states.values():
        obj_list.append(state_obj)
    for state in obj_list:
        if state.id == state_id:
            for k, v in content.items():
                setattr(state, k, v)
            new_state = state
    if new_state is None:
        return jsonify({"error": "Not found"}), 404
    storage.save()
    return jsonify(new_state.to_dict()), 200
"""
