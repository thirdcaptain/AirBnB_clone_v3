#!/usr/bin/python3
"""
    Handles RESTful API actions for Place objects
"""


from models import BaseModel
from models import storage
from api.v1.views import app_views
from flask import jsonify
from flask import make_response
from flask import abort
from flask import request
from models import Place


@app_views.route("/cities/<city_id>/places")
def places(city_id):
    """
    prints all places
    """
    obj_list = []
    json_list = []
    json_places = storage.all("Place")
    for place_obj in json_places.values():
        obj_list.append(place_obj)
    for place in obj_list:
        if place.city_id == city_id:
            json_list.append(place.to_dict())
    return jsonify(json_list)


@app_views.route("/places/<place_id>", methods=['GET'])
def get_place(place_id):
    """
    get place
    """
    get_place = storage.get("Place", place_id)
    if get_place is None:
        abort(404)
    return jsonify(get_place.to_dict()), 200


@app_views.route("/places/<place_id>", methods=['DELETE'])
def delete_place(place_id):
    """
    delete place
    """
    empty_dict = {}

    try:
        json_place = storage.get("Place", place_id)
        json_place.delete()
        storage.save()
        return jsonify(empty_dict), 200
    except Exception:
        abort(404)


@app_views.route("/cities/<city_id>/places", methods=['POST'])
def post_place(city_id):
    """
    post a place
    """
    content = request.get_json()
    if content is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in content:
        return jsonify({"error": "Missing user_id"}), 400
    if "name" not in content:
        return jsonify({"error": "Missing name"}), 400

    try:
        place_user_id = content["user_id"]
        place_name = content["name"]
        new_place = Place(user_id=place_user_id, name=place_name)
        for k, v in content.items():
            setattr(new_place, k, v)
        setattr(new_place, "city_id", city_id)
        storage.save()
        return jsonify(new_place.to_dict()), 201

    except Exception:
        abort(404)


@app_views.route("/places/<place_id>", methods=['PUT'])
def put_place(place_id):
    """
    put a place
    """
    obj_list = []
    content = request.get_json()
    exclude = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']

    try:
        place_obj = storage.get('Place', place_id)
        if place_obj is None:
            abort(404)
        if content is None:
            return jsonify({"error": "Not a JSON"}), 400
        for k, v in content.items():
            if k not in exclude:
                setattr(place_obj, k, v)
        place_obj.save()
        return jsonify(place_obj.to_dict()), 200
    except Exception:
        abort(404)
