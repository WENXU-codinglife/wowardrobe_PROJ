import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from models import ItemsModel
from schemas import ItemSchema, ItemUpdateSchema

from db import db
from utils.utils import strToDatetime
from utils.query import query_chaining_filter, query_chaining_limit, query_chaining_page, query_chaining_sort



blp = Blueprint("Items", "items", description = "Operations on items")

ATTRIBUTES_EQUAL = ['item_category', 'item_color', 'item_season', 'item_suitability'] # query only for equal to a value
ATTRIBUTES_RANGE = ['item_price', 'item_time'] # query can be >, <, <=, >=
ATTRIBUTES_ALL = [*ATTRIBUTES_EQUAL, *ATTRIBUTES_RANGE]
OPERATORS = ['>=', '<=', '>', '<']

@blp.route("/itemsList")
class ItemsList(MethodView):
    # get all items 
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        query = ItemsModel.query
        query = query_chaining_filter(query, ItemsModel, request, ATTRIBUTES_ALL)     
        query = query_chaining_sort(query, ItemsModel, request, ATTRIBUTES_ALL)     
        query = query_chaining_limit(query, request)     
        query = query_chaining_page(query, request)     
        return query.all()

    # create a new item
    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, request):
        item_id = uuid.uuid4().hex
        while ItemsModel.query.get(item_id):
            item_id = uuid.uuid4().hex
            
        request["item_time"] = strToDatetime(request["item_time"])
        print(request["item_time"])
        new_item = ItemsModel(item_id=item_id, **request)

        try:
            db.session.add(new_item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")
        return new_item

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
        item.item_time = strToDatetime(request["item_time"])
        item.item_season = request["item_season"]
        item.wardrobe_id = request["wardrobe_id"]

        try:
            db.session.delete(item)
            db.session.commit()
        except SQLAlchemyError:
             abort(500, message="An error occurred creating the store.")

        return item

