from db import db

class WardrobesModel(db.Model):
    __tablename__ = "wardrobes"
    wardrobe_id = db.Column(db.String, primary_key = True)
    user_id = db.Column(db.String, db.ForeignKey("users.user_id"), unique=False, nullable = False)
    wardrobe_name = db.Column(db.String, unique=False, nullable = False)
    wardrobe_image = db.Column(db.String, unique=False)

    user = db.relationship("UsersModel", back_populates="wardrobes")
    items = db.relationship("ItemsModel", back_populates="wardrobe", lazy="dynamic")
