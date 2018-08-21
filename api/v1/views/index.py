#!/usr/bin/python3
"""
    Create a route /status on the object app_views that reutns a JSON
"""


from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    json_status = {"status": "OK"}
    return jsonify(json_status)
