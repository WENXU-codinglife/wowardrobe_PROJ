from db import db

class ImagesModel(db.Model):
    __tablename__ = "images"
    image_id = db.Column(db.String, primary_key=True)
    url = db.Column(db.String, nullable=False)

    item_id = db.Column(db.String, db.ForeignKey("items.item_id"),unique=False, nullable=False)
    item = db.relationship("ItemsModel", back_populates="images")