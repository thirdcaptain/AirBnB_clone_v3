#!/usr/bin/python3
"""
    Handles RESTful API actions for State objects
"""


from models import BaseModel
from models import storage
from api.v1.views import app_views
from flask import jsonify
from flask import make_response
from flask import abort
from flask import request
from models import State


@app_views.route("/states")
def states():
    """
    prints all states
    """
    obj_list = []
    json_list = []
    json_states = storage.all("State")
    for state_obj in json_states.values():
        obj_list.append(state_obj)
    for state in obj_list:
        json_list.append(state.to_dict())
    return jsonify(json_list)


@app_views.route("/states/<state_id>", methods=['GET'])
def get_states(state_id):
    """
    gets state from uuid
    """
    get_state = storage.get("State", state_id)
    if get_state is None:
        abort(404)
    return jsonify(get_state.to_dict()), 200


@app_views.route("/states/<state_id>", methods=['DELETE'])
def delete_states(state_id):
    """
    deletes a state
    """
    empty_dict = {}

    try:
        json_states = storage.get("State", state_id)
        json_states.delete()
        storage.save()
        return jsonify(empty_dict), 200
    except Exception:
        abort(404)


@app_views.route("/states", methods=['POST'])
def post_states():
    """
    post method
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
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'])
def put_states(state_id):
    """
    put method
    """
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
