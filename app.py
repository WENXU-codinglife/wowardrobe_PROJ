import os
from flask import Flask
from flask_smorest import Api

from db import db
import models

from resources.items import blp as ItemsBlueprint
from resources.wardrobes import blp as WardrobesBlueprint
from resources.users import blp as UsersBlueprint
from resources.images import blp as ImagesBlueprint


def create_app(db_url=None):
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "WoWardrobe REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(UsersBlueprint)
    api.register_blueprint(WardrobesBlueprint)
    api.register_blueprint(ItemsBlueprint)
    api.register_blueprint(ImagesBlueprint)

    return app