from flask import Flask
from flask_smorest import Api

from resources.items import blp as ItemsBlueprint
from resources.wardrobes import blp as WardrobesBlueprint


app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"

api = Api(app)

api.register_blueprint(ItemsBlueprint)
api.register_blueprint(WardrobesBlueprint)