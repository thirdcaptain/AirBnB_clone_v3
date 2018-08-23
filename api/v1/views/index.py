#!/usr/bin/python3
"""
    Create a route /status on the object app_views that reutns a JSON
"""

from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """
    Status for ok
    """
    json_status = {"status": "OK"}
    return jsonify(json_status)


@app_views.route("/stats")
def stats():
    """
    Endpoint that retrieves the number of each objects by type
    """
    json_stats = {"amenities": storage.count("Amenity"),
                  "cities": storage.count("City"),
                  "places": storage.count("Place"),
                  "reviews": storage.count("Review"),
                  "states": storage.count("State"),
                  "users": storage.count("User")}
    return jsonify(json_stats)
