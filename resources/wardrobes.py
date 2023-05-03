from email import message
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from resources.db import Wardrobes as wardrobes
from schemas import WardrobeSchema, WardrobeUpdateSchema

blp = Blueprint("Wardrobes", __name__, description = "Operations on wardrobes")


@blp.route("/wardrobesList/<string:user_id>")
class WardrobesList(MethodView):
    # get all wardrobes
    @blp.response(200, WardrobeSchema(many=True))
    def get(cls, user_id):
        return [w for w in wardrobes.values() if w["user_id"] ==  user_id]

    # create a new wardrobe
    @blp.arguments(WardrobeSchema)
    @blp.response(201, WardrobeSchema)
    def post(cls, request, user_id):
        wardrobe_name = request.get("wardrobe_name")
        user_wardrobe = [w for w in wardrobes.values() if w["user_id"] ==  user_id and w["wardrobe_name"] == wardrobe_name]
        if len(user_wardrobe) > 0:
            abort(400, message=f"Wardrobe name already exists!")
        wardrobe_images = request.get("wardrobe_images")
        wardrobe_id = uuid.uuid4().hex
        # take care of duplicate names case
        new_wardrobe = {
            "wardrobe_name": wardrobe_name, 
            "wardrobe_id": wardrobe_id,
            "user_id": user_id,
            "wardrobe_images": wardrobe_images
        }
        wardrobes[wardrobe_id] = new_wardrobe
        return new_wardrobe


@blp.route("/wardrobes/<string:user_id>/<string:wardrobe_id>")
class Wardrobes(MethodView):
    # update an existing wardrobe
    @blp.arguments(WardrobeUpdateSchema)
    @blp.response(201, WardrobeSchema)
    def put(cls, request, user_id, wardrobe_id):
        if wardrobe_id not in wardrobes or wardrobes[wardrobe_id]["user_id"] != user_id:
            abort(400, message=f"Wardrobe doesn't exist!")
        wardrobes[wardrobe_id].update(request)
        return wardrobes[wardrobe_id]

    
