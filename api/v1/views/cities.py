#!/usr/bin/python3
"""
    Handles RESTful API actions for cities objects
"""


from models import storage
from api.v1.views import app_views
from flask import jsonify
from flask import make_response
from flask import abort
from flask import request
from models import City


@app_views.route("/states/<state_id>/cities")
def cities(state_id):
    """
    prints all cities
    """
    obj_list = []
    json_list = []
    json_cities = storage.all("City")

    for city_obj in json_cities.values():
        obj_list.append(city_obj)

    for city in obj_list:
        if city.state_id == state_id:
            json_list.append(city.to_dict())
            return jsonify(json_list), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route("/cities/<city_id>", methods=['GET'])
def get_cities(city_id):
    """
    Get a city using a the city_id
    """
    get_city = storage.get("City", city_id)
    if get_city is None:
        abort(404)
    return jsonify(get_city.to_dict()), 200


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def delete_cities(city_id):
    """
    Use the city_id to delete the city
    """
    empty_dict = {}

    try:
        json_city = storage.get("City", city_id)
        json_city.delete()
        storage.save()
        return jsonify(empty_dict), 200
    except Exception:
        abort(404)


@app_views.route("/states/<state_id>/cities", methods=['POST'])
def post_cities(state_id):
    """
    City Post method
    """
    content = request.get_json()
    get_state = storage.all("State")
    obj_list = []

    if content is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in content:
        return jsonify({"error": "Missing name"}), 400

    for state_obj in get_state.values():
        obj_list.append(state_obj)
    for state in obj_list:
        if state.id == state_id:
            new_city = City(**content)
            setattr(new_city, "state_id", state_id)
            storage.new(new_city)
            storage.save()
            return jsonify(new_city.to_dict()), 201
    return jsonify({"error": "Not found"}), 404


@app_views.route("/cities/<city_id>", methods=['PUT'])
def put_cities(city_id):
    """
    Put method for cities
    """
    new_city = None
    content = request.get_json()
    obj_list = []
    exclude = ['id', 'created_at', 'updated_at']
    get_city = storage.all("City")

    if content is None:
        return jsonify({"error": "Not a JSON"}), 400

    for e in exclude:
        content.pop(e, None)

    for city_obj in get_city.values():
        obj_list.append(city_obj)

    for city in obj_list:
        if city.id == city_id:
            for k, v in content.items():
                setattr(city, k, v)
            new_city = city
    storage.save()
    if new_city is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(new_city.to_dict()), 200
