from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from db import db
from config import app_config
from resources.items import MenuItems, Products, ShopItems
from resources.users import UserRegister


def create_app(config_name):
    flask_app = Flask(__name__)
    flask_app.config.from_object(app_config[config_name])
    flask_app.config.from_pyfile('config.py')
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    api = Api(flask_app)

    api.add_resource(MenuItems, '/menu')
    api.add_resource(ShopItems, '/shop')
    api.add_resource(Products, '/shop/<string:title>')
    api.add_resource(UserRegister, '/user/register')
    db.init_app(flask_app)

    CORS(flask_app)

    return flask_app
