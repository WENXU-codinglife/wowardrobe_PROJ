import os
from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from db import db
from whitelist import WHITELIST

from resources.items import blp as ItemsBlueprint
from resources.wardrobes import blp as WardrobesBlueprint
from resources.users import blp as UsersBlueprint
from resources.images import blp as ImagesBlueprint


def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "WoWardrobe REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app,db)

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "sean"
    jwt = JWTManager(app)
    '''
    Should generate a long and random secret key using something 
    like str(secrets.SystemRandom().getrandbits(128)).
    '''
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.token_in_blocklist_loader
    def check_if_token_not_in_whitelist(jwt_header, jwt_payload):
        return jwt_payload["jti"] not in WHITELIST


    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    # using Flask-Migrate to create our database, so no longer need to 
    # tell Flask-SQLAlchemy to do it when creating the app
    # with app.app_context():
    #     db.create_all()

    api.register_blueprint(UsersBlueprint)
    api.register_blueprint(WardrobesBlueprint)
    api.register_blueprint(ItemsBlueprint)
    api.register_blueprint(ImagesBlueprint)

    return app