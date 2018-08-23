#!/usr/bin/python3
"""
    Handles RESTful API actions for Review objects
"""


from models import BaseModel
from models import storage
from api.v1.views import app_views
from flask import jsonify
from flask import make_response
from flask import abort
from flask import request
from models import Review


@app_views.route("/places/<place_id>/reviews")
def reviews(place_id):
    """
    prints all reviews
    """
    obj_list = []
    json_list = []
    json_reviews = storage.all("Review")
    for review_obj in json_reviews.values():
        obj_list.append(review_obj)
    for review in obj_list:
        if review.place_id == place_id:
            json_list.append(review.to_dict())
    if len(json_list) > 0:
        return jsonify(json_list)
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=['GET'])
def get_review(review_id):
    """
    get a review
    """
    get_review = storage.get("Review", review_id)
    if get_review is None:
        abort(404)
    return jsonify(get_review.to_dict()), 200


@app_views.route("/reviews/<review_id>", methods=['DELETE'])
def delete_review(review_id):
    """
    delete a review
    """
    empty_dict = {}

    try:
        json_review = storage.get("Review", review_id)
        json_review.delete()
        storage.save()
        return jsonify(empty_dict), 200
    except Exception:
        abort(404)


@app_views.route("/places/<place_id>/reviews", methods=['POST'])
def post_review(place_id):
    """
    post a review
    """
    content = request.get_json()
    if content is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in content:
        return jsonify({"error": "Missing user_id"}), 400
    if "text" not in content:
        return jsonify({"error": "Missing text"}), 400

    try:
        new_review = Review(user_id=content["user_id"],
                            place_id=place_id,
                            text=content["text"])
        for k, v in content.items():
            setattr(new_review, k, v)
        storage.save()
        return jsonify(new_review.to_dict()), 201

    except Exception:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=['PUT'])
def put_review(review_id):
    """
    puts a review
    """
    obj_list = []
    content = request.get_json()
    exclude = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']

    try:
        review_obj = storage.get('Review', review_id)
        if review_obj is None:
            abort(404)
        if content is None:
            return jsonify({"error": "Not a JSON"}), 400
        for k, v in content.items():
            if k not in exclude:
                setattr(review_obj, k, v)
        review_obj.save()
        return jsonify(review_obj.to_dict()), 200
    except Exception:
        abort(404)
