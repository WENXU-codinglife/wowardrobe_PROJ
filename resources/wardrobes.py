import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import WardrobeSchema, WardrobeUpdateSchema
from models import WardrobesModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("Wardrobes", "wardrobes", description = "Operations on wardrobes")


@blp.route("/wardrobe/<string:wardrobe_id>")
class Wardrobe(MethodView):
    # get a wardrobe
    @blp.response(200, WardrobeSchema)
    def get(self, wardrobe_id):
        wardrobe = WardrobesModel.query.get_or_404(wardrobe_id) # get_or_404 takes primary key as argument
        return wardrobe

    def delete(self, wardrobe_id):
        wardrobe = WardrobesModel.query.get_or_404(wardrobe_id)
        db.session.delete(wardrobe)
        db.session.commit()
        return  {"message": f"Wardrobe '{wardrobe.wardrobe_name}' deleted!"}, 200

    @blp.arguments(WardrobeUpdateSchema)
    @blp.response(200, WardrobeSchema)
    def put(self, request, wardrobe_id):
        wardrobe = WardrobesModel.query.get_or_404(wardrobe_id)
        user_id = wardrobe.user_id
        duplicateName = WardrobesModel.query.filter_by(wardrobe_id!=wardrobe_id, user_id=user_id, wardrobe_name=request["wardrobe_name"])
        if duplicateName:
            abort(400, message=f"Wardrobe name {duplicateName.wardrobe_name} already exists!")

        wardrobe.wardrobe_name = request["wardrobe_name"]
        wardrobe.wardrobe_image = request["wardrobe_image"]

        db.session.add(wardrobe)
        db.session.commit()

        return wardrobe

@blp.route("/wardrobesList")
class WardrobesList(MethodView):
    # get all wardrobes 
    @blp.response(200, WardrobeSchema(many=True))
    def get(self):
        return WardrobesModel.query.all()

    # create a new wardrobe
    @blp.arguments(WardrobeSchema)
    @blp.response(201, WardrobeSchema)
    def post(self, request):
        wardrobe_name = request["wardrobe_name"]
        wardrobe_image = request["wardrobe_image"]
        user_id = request["user_id"]
        exsiting_wardrobe = WardrobesModel.query.filter_by(user_id=user_id, wardrobe_name=wardrobe_name).first()
        if exsiting_wardrobe is not None:
            abort(400, message=f"Wardrobe name {wardrobe_name} already exists!")
        wardrobe_id = uuid.uuid4().hex
        new_wardrobe = WardrobesModel(**{
            "wardrobe_name": wardrobe_name, 
            "wardrobe_id": wardrobe_id,
            "user_id": user_id,
            "wardrobe_image": wardrobe_image
        })
        
        db.session.add(new_wardrobe)
        db.session.commit()
        return new_wardrobe
