from flask_restful import Resource
from models.menu_item import MenuItem


class MenuItems(Resource):
    def get(self):
        return {"menuItems": [item.json() for item in MenuItem.find_all()]}
