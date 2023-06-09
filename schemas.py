from enum import unique
from marshmallow import Schema, fields

from models import wardrobe

class PlainUserSchema(Schema):
    user_id = fields.String(dump_only=True)
    user_name = fields.String()
    user_email = fields.String(required=True, metadata={'unique': True})
    user_password = fields.String(required=True, load_only=True)

class PlainWardrobeSchema(Schema):
    wardrobe_id = fields.String(dump_only=True)
    wardrobe_name = fields.String(required=True)
    wardrobe_image = fields.String(required=False)
    wardrobe_description = fields.String(required=False)

class PlainItemSchema(Schema):
    item_id = fields.String(dump_only=True)
    item_color = fields.String(required=True)
    item_category = fields.String(required=True)
    item_suitability = fields.String(required=True)
    item_price = fields.Float(required=True)
    item_time = fields.String(required=True)
    item_season = fields.String(required=True)

class PlainImageSchema(Schema):
    image_id = fields.String(dump_only=True)
    url = fields.String(required=True)

class UserSchema(PlainUserSchema):
    wardrobes = fields.List(fields.Nested(PlainWardrobeSchema()), dump_only=True)


class WardrobeSchema(PlainWardrobeSchema):
    user_id = fields.String(required=True, load_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)

class ItemSchema(PlainItemSchema):
    wardrobe_id = fields.String(required=True, load_only=True)
    wardrobe = fields.Nested(PlainWardrobeSchema(), dump_only=True)
    images = fields.List(fields.Nested(PlainImageSchema()), dump_only=True)

class ImageSchema(PlainImageSchema):
    item_id = fields.String(required=True, load_only=True)
    item = fields.Nested(PlainItemSchema(), dump_only=True)


class WardrobeUpdateSchema(Schema):
    wardrobe_name = fields.String()
    wardrobe_image = fields.String()  
    wardrobe_description = fields.String()

class ItemUpdateSchema(Schema):
    item_color = fields.String()
    item_category = fields.String()
    item_suitability = fields.String()
    item_price = fields.Float()
    item_time = fields.String()
    item_season = fields.String()
    wardrobe_id = fields.String()