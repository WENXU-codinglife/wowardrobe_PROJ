from sqlalchemy import Enum
from db import db

class ItemsModel(db.Model):
    __tablename__ = "items"
    item_id = db.Column(db.String, primary_key = True)
    item_color = db.Column(db.String, unique=False, nullable=False)
    item_category = db.Column(db.String, unique=False, nullable=False)
    item_suitability = db.Column(db.String, unique=False, nullable=False)
    item_price = db.Column(db.Float, unique=False, nullable=False)
    item_time = db.Column(db.DateTime, unique=False, nullable=False)
    item_season = db.Column(Enum('spring', 'summer', 'fall', 'winter', name="season_name"), unique=False, nullable=False)
    wardrobe_id = db.Column(db.String, db.ForeignKey("wardrobes.wardrobe_id"), unique=False, nullable = False)

    wardrobe = db.relationship("WardrobesModel", back_populates="items")
    images = db.relationship("ImagesModel", back_populates="item", lazy="dynamic")
