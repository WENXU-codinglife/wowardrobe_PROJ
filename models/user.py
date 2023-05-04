from db import db

class UsersModel(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.String, primary_key = True)
    user_name = db.Column(db.String, nullable = False)
    user_email = db.Column(db.String, unique = True, nullable = False)
    user_password = db.Column(db.String, nullable = False)

    wardrobes = db.relationship("WardrobesModel", back_populates="user", lazy="dynamic")
