import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import ItemsModel
from schemas import ItemSchema, ItemUpdateSchema
from db import db
from datetime import datetime


blp = Blueprint("Items", "items", description = "Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    # get a item
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemsModel.query.get_or_404(item_id) # get_or_404 takes primary key as argument
        return item

    def delete(self, item_id):
        item = ItemsModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return  {"message": f"Item deleted!"}, 200

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
        db.session.add(item)
        db.session.commit()

        return item

@blp.route("/itemsList")
class ItemsList(MethodView):
    # get all items 
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemsModel.query.all()

    # create a new item
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, request):
        item_id = uuid.uuid4().hex
        while ItemsModel.query.get(item_id):
            item_id = uuid.uuid4().hex
            
        request["item_time"] = datetime.strptime(request["item_time"],'%Y-%m-%d')
        new_item = ItemsModel(item_id=item_id, **request)

        db.session.add(new_item)
        db.session.commit()
        return new_item
