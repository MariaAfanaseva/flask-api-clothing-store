from flask_restful import Resource
from models.menu_items import MenuItemsModel


class MenuItems(Resource):
    def get(self):
        return {"menuItems": [item.json() for item in MenuItemsModel.find_all()]}
