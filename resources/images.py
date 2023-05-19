import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from models import ImagesModel
from schemas import ImageSchema
from db import db


blp = Blueprint("Images", "images", description = "Operations on images")


@blp.route("/image/<string:image_id>")
class Image(MethodView):
    # get an image
    @jwt_required()
    @blp.response(200, ImageSchema)
    def get(self, image_id):
        image = ImagesModel.query.get_or_404(image_id) # get_or_404 takes primary key as argument
        return image

    @jwt_required()
    def delete(self, image_id):
        image = ImagesModel.query.get_or_404(image_id)
        db.session.delete(image)
        db.session.commit()
        return  {"message": f"Image deleted!"}, 200

@blp.route("/imagesListAll")
class ImagesListAll(MethodView):
    # get all images 
    @jwt_required()
    @blp.response(200, ImageSchema(many=True))
    def get(self):
        return ImagesModel.query.all()

    # # create a new image
    # @jwt_required()
    # @blp.arguments(ImageSchema)
    # @blp.response(201, ImageSchema)
    # def post(self, request):
    #     image_id = uuid.uuid4().hex
    #     while ImagesModel.query.get(image_id):
    #         image_id = uuid.uuid4().hex
    #     new_image = ImagesModel(image_id=image_id, **request)

    #     db.session.add(new_image)
    #     db.session.commit()
    #     return new_image

@blp.route("/imagesUpload")
class ImagesUpload(MethodView):
    @jwt_required()
    @blp.arguments(ImageSchema(many=True))
    @blp.response(201)
    def post(self, request):
        new_images = []
        for img in request:
            item_id = img["item_id"]
            url = img["url"]
            image_id = uuid.uuid4().hex
            while ImagesModel.query.get(image_id):
                image_id = uuid.uuid4().hex
            new_image = ImagesModel(image_id=image_id, item_id=item_id, url=url)
            db.session.add(new_image) 
            new_images.append({
                "image_url": url
            })                
        db.session.commit()
        return new_images