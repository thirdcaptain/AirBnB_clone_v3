#!/usr/bin/python3
"""
    Handles RESTful API actions for amenities objects
"""


from models import BaseModel
from models import storage
from api.v1.views import app_views
from flask import jsonify
from flask import make_response
from flask import abort
from flask import request
from models import Amenity


@app_views.route("/amenities")
def amenities():
    """
    prints all amenities
    """
    obj_list = []
    json_list = []
    json_amenities = storage.all("Amenity")
    for amenities_obj in json_amenities.values():
        obj_list.append(amenities_obj)
    for amenity in obj_list:
        json_list.append(amenity.to_dict())
    return jsonify(json_list)


@app_views.route("/amenities/<amenity_id>", methods=['GET'])
def get_amenity(amenity_id):
    """
    gets an amenity
    """
    get_amenity = storage.get("Amenity", amenity_id)
    if get_amenity is None:
        abort(404)
    return jsonify(get_amenity.to_dict()), 200


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'])
def delete_amenity(amenity_id):
    """
    Deletes an amenity
    """
    empty_dict = {}
    try:
        json_amenity = storage.get("Amenity", amenity_id)
        json_amenity.delete()
        storage.save()
        return jsonify(empty_dict), 200
    except Exception:
        abort(404)


@app_views.route("/amenities", methods=['POST'])
def post_amenities():
    """
    Creates an amenity
    """
    content = request.get_json()
    if content is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in content:
        return jsonify({"error": "Missing name"}), 400
    exclude = ['id', 'created_at', 'updated_at']
    for e in exclude:
        content.pop(e, None)
    new_amenity = Amenity(**content)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'])
def put_amenities(amenity_id):
    """
    Updates an amenity
    """
    new_amenity = None
    obj_list = []
    content = request.get_json()
    if content is None:
        return jsonify({"error": "Not a JSON"}), 400
    exclude = ['id', 'created_at', 'updated_at']
    for e in exclude:
        content.pop(e, None)
    json_amenities = storage.all("Amenity")
    for amenity_obj in json_amenities.values():
        obj_list.append(amenity_obj)
    for amenity in obj_list:
        if amenity.id == amenity_id:
            for k, v in content.items():
                setattr(amenity, k, v)
            new_amenity = amenity
    if new_amenity is None:
        return jsonify({"error": "Not found"}), 404
    storage.save()
    return jsonify(new_amenity.to_dict()), 200
