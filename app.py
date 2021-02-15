import os
from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
from flask_cors import CORS
from db import db
from resources.items import MenuItems, Products, ShopItems
from fill_db import UpdateDb

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api(app)
load_dotenv('.env')

DEBUG = (os.getenv('DEBUG') == 'True')

api.add_resource(MenuItems, '/menu')
api.add_resource(Products, '/<string:title>')
api.add_resource(ShopItems, '/shop')

db.init_app(app)


@app.before_first_request
def update_db():
    if os.getenv('FILL_DB') == 'True':
        update = UpdateDb()
        update.recreate_db()


CORS(app)

if __name__ == "__main__":
    app.run(port=5000, debug=DEBUG)
