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


@app_views.route("/users", methods=['POST'])
def post_user():
    """
    posts a user
    """
    content = request.get_json()
    if content is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in content:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in content:
        return jsonify({"error": "Missing password"}), 400

    user_email = content["email"]
    user_password = content["password"]
    new_user = User(email=user_email, password=user_password)
    for k, v in content.items():
        setattr(new_user, k, v)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'])
def put_user(user_id):
    """
    Updates a user
    """
    obj_list = []
    content = request.get_json()
    user_obj = storage.get('User', user_id)
    exclude = ['id', 'created_at', 'updated_at']

    if user_obj is None:
        abort(404)
    if content is None:
        return jsonify({"error": "Not a JSON"}), 400
    for k, v in content.items():
        if k not in exclude:
            setattr(user_obj, k, v)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200
