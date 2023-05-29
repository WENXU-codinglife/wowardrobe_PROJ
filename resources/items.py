import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from models import ItemsModel
from schemas import ItemSchema, ItemUpdateSchema
from flask_jwt_extended import jwt_required
from db import db
from datetime import datetime


blp = Blueprint("Items", "items", description = "Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    # get a item
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemsModel.query.get_or_404(item_id) # get_or_404 takes primary key as argument
        return item

    def delete(self, item_id):
        item = ItemsModel.query.get_or_404(item_id)

        try:
            db.session.delete(item)
            db.session.commit()
        except SQLAlchemyError:
             abort(500, message="An error occurred creating the store.")

        return  {"message": f"Item deleted!"}, 200
    
    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, request, item_id):
        item = ItemsModel.query.get_or_404(item_id)
        item.item_color = request["item_color"]
        item.item_category = request["item_category"]
        item.item_suitability = request["item_suitability"]
        item.item_price = request["item_price"]
        item.item_time = datetime.strptime(request["item_time"],'%Y-%m-%d')
        item.item_season = request["item_season"]
        item.wardrobe_id = request["wardrobe_id"]

        try:
            db.session.delete(item)
            db.session.commit()
        except SQLAlchemyError:
             abort(500, message="An error occurred creating the store.")

        return item

@blp.route("/itemsList")
class ItemsList(MethodView):
    # get all items 
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemsModel.query.all()

    # create a new item
    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, request):
        item_id = uuid.uuid4().hex
        while ItemsModel.query.get(item_id):
            item_id = uuid.uuid4().hex
            
        request["item_time"] = datetime.strptime(request["item_time"],'%Y-%m-%d')
        new_item = ItemsModel(item_id=item_id, **request)

        try:
            db.session.add(new_item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")
            
        return new_item
