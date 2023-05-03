import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import Items as items
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint("Items", "items", description = "Operations on items")


@blp.route("/itemsList")
class itemsList(MethodView):
    # get all items
    def get(self):
        
        return {"items": items}

    # create a new item 
    def post(self):
        request_data = request.get_json()
        item_id,user_id,wardrobe_id,item_color, item_category,item_suitability,item_price, \
        item_time, item_season, item_images = request_data.values()
        # take care of duplicate names case
        new_item = {
            "item_id" : item_id,
            "user_id" : user_id, 
            "wardrobe_id" : wardrobe_id,
            "item_color" : item_color, 
            "item_category" : item_category,
            "item_suitability" : item_suitability,
            "item_price" : item_price,
            "item_time" : item_time, 
            "item_season" : item_season, 
            "item_images" : item_images
        }
        items[item_id] = new_item
        return new_item, 201


    # update an existing item

