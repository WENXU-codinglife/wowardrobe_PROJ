import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, decode_token
from passlib.hash import pbkdf2_sha256
from schemas import UserSchema
from models import UsersModel
from db import db
from whitelist import WHITELIST

blp = Blueprint("Users", "users", description = "Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, request):
        user_email = request["user_email"]
        user_name = request["user_name"]
        user_password = request["user_password"]
        if UsersModel.query.filter_by(user_email = user_email).first():
            abort(409, message="A user with that username already exists.")

        user_id = uuid.uuid4().hex
        while UsersModel.query.get(user_id):
            user_id = uuid.uuid4().hex

        new_user = UsersModel(**{
            "user_id": user_id, 
            "user_name": user_name,
            "user_email": user_email,
            "user_password": pbkdf2_sha256.hash(user_password)
        })
        db.session.add(new_user)
        db.session.commit()
        return new_user

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, request):
        user = UsersModel.query.filter(
            UsersModel.user_email == request["user_email"]
        ).first()

        if user and pbkdf2_sha256.verify(request["user_password"], user.user_password):
            access_token = create_access_token(identity=user.user_id)
            jti = decode_token(access_token)["jti"]
            WHITELIST.add(jti)
            print(WHITELIST)
            return {"access_token": access_token}, 200

        abort(401, message="Invalid credentials.")        

@blp.route("/user")
class Users(MethodView):
    # get all users - ONLY FOR TESTING
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UsersModel.query.all()


@blp.route("/user/<string:user_id>")
class User(MethodView):
    # get a user - ONLY FOR TESTING
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UsersModel.query.get_or_404(user_id) # get_or_404 takes primary key as argument
        return user

    def delete(self, user_id):
        user = UsersModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return  {"message": f"User '{user.user_email}' deleted!"}, 200

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        WHITELIST.remove(jti)
        return {"message": "Successfully logged out"}, 200