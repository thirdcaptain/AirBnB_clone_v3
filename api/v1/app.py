#!/usr/bin/python3
"""Flask web app"""


import os
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import jsonify
from flask import make_response
from flask_cors import CORS


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views, url_prefix='/api/v1')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """
    Teardown method to clean up
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """
    Error method
    """
    error_status = {"error": "Not found"}
    return make_response(jsonify(error_status), 404)


if __name__ == "__main__":
    hosts = os.getenv("HBNB_API_HOST", default='0.0.0.0')
    ports = int(os.getenv("HBNB_API_PORT", default=5000))
    app.run(host=hosts, port=ports, threaded=True)
