from flask_restful import Resource
from models.menu_item import MenuItem


class MenuItems(Resource):
    def get(self):
        return {"menuItems": [item.json() for item in MenuItem.find_all()]}


class Products(Resource):
    def get(self, title):
        products = MenuItem.query.filter_by(title=title).first().products
        if products:
            return {"products": [x.json() for x in products]}
        else:
            return {'error': 'Not found'}


class ShopItems(Resource):
    def get(self):
        response = []
        for menu in MenuItem.find_all():
            print(menu.products)
        # return {"shopItems": [item.json()  for item in MenuItem.find_all()]}
