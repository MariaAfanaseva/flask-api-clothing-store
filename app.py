from flask import Flask
from db import db
from flask_restful import Api
from resources.menu_items import MenuItems
from fill_db import UpdateDb


app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api(app)


@app.before_first_request
def fill_db():
    update_db = UpdateDb()
    update_db.recreate_db()


api.add_resource(MenuItems, "/menu")

db.init_app(app)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
