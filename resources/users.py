import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import UserSchema
from models import UsersModel
from db import db

blp = Blueprint("Users", "users", description = "Operations on users")


@blp.route("/user")
class Users(MethodView):
    # get all users
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UsersModel.query.all()

    # create a new user
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, request):
        user_id = uuid.uuid4().hex
        user_name = request["user_name"]
        user_email = request["user_email"]
        user_password = request["user_password"]
        new_user = UsersModel(**{
            "user_id": user_id, 
            "user_name": user_name,
            "user_email": user_email,
            "user_password": user_password
        })
        db.session.add(new_user)
        db.session.commit()
        return new_user

@blp.route("/user/<string:user_id>")
class User(MethodView):
    # get a user
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UsersModel.query.get_or_404(user_id) # get_or_404 takes primary key as argument
        return user

    def delete(self, user_id):
        user = UsersModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return  {"message": f"User '{user.user_email}' deleted!"}, 200