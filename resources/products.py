from flask_restful import Resource
from models.menu_item import MenuItem


class Products(Resource):
    def get(self, title):
        products = MenuItem.query.filter_by(title=title).first().products
        if products:
            return {"products": [x.json() for x in products]}
        else:
            return {'error': 'Not found'}

