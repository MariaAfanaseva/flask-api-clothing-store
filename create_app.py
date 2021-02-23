from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from databases.db import db
from configs.config import app_config
from resources.items import MenuItems, Products, ShopItems
from resources.users import (
    UserRegister, UserLogin,
    UserLogout, TokenRefresh
)
from databases.redis_db import is_jti_blocklisted


def create_app(config_name):
    flask_app = Flask(__name__)
    flask_app.config.from_object(app_config[config_name])
    flask_app.config.from_pyfile('configs/config.py')

    api = Api(flask_app)

    api.add_resource(MenuItems, '/menu')
    api.add_resource(ShopItems, '/shop')
    api.add_resource(Products, '/shop/<string:title>')
    api.add_resource(UserRegister, '/user/register')
    api.add_resource(UserLogin, '/user/login')
    api.add_resource(UserLogout, '/user/logout')
    api.add_resource(TokenRefresh, '/user/refresh')
    db.init_app(flask_app)

    flask_app.secret_key = flask_app.config['SECRET']
    jwt = JWTManager(flask_app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        """
         This method will check if a token is blacklisted,
         and will be called automatically when blacklist is enabled
        """
        return (
            is_jti_blocklisted(jwt_payload["jti"])
        )

    CORS(flask_app)

    return flask_app
