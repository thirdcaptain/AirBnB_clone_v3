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
    try:
       get_state = storage.get("State", state_id)
       return jsonify(get_state.to_dict()), 200
    except Exception:
        abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'])
def delete_states(state_id):
    """
    deletes a state
    """
    empty_dict = {}
    obj_list = []
    json_list = []

    try:
        json_states = storage.all("State")
        for state_obj in json_states.values():
            obj_list.append(state_obj)
        for state_obj in obj_list:
            if state_obj.id == state_id:
                storage.delete(state_obj)
                storage.save()
                return jsonify(empty_dict), 200
    except Exception:
        abort(404)
    abort(404)


@app_views.route("/states", methods=['POST'])
def post_states():
    content = request.get_json()
    print(content)
    print(type(content))
    #KWARGS method
    new_state = State(**content)

    #SETATTR method
#    for key, value in content.items():
#        setattr(new_state, key, value)

#    print(new_state)
#    new_state(content)
#    print(new_state)
#    print("new_state")
#    print(new_state)
#    print("new_state.id")
#    print(new_state.id)
#    print("new_state.name")
#    print(new_state.name)
#    setattr(new_state, "name", "LisaLand")
#    print("new_state after SETATTR")
#    print(new_state)

    return jsonify(new_state.to_dict())
