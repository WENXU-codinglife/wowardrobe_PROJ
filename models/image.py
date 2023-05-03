from db import db

class ImagesModel(db.Model):
    __tablename__ = "images"
    url = db.Column(db.String, nullable=False)
    item_id = db.Column(db.String, db.ForeignKey("items.item_id"), nullable=False)

    item = db.relationship("ItemsModel", back_populates="images")