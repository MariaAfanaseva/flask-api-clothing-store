from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from models.menu_item import MenuItem
from models.user import User


def request_parser(*args):
    parser = reqparse.RequestParser()
    for arg in args:
        if arg == 'id':
            parser.add_argument(
                arg, type=int, required=True, help="id field must be integer."
            )
        parser.add_argument(
            arg, type=str, required=True, help=f"{arg} field cannot be blank."
        )
    return parser


class MenuItems(Resource):
    def get(self):
        return {"menuItems": [item.json() for item in MenuItem.find_all()]}

    @jwt_required(refresh=True)
    def post(self):
        user_email = get_jwt_identity()
        if User.find_by_email(user_email).is_admin:
            data = request_parser('title', 'imageUrl', 'size', 'linkUrl').parse_args()
            if MenuItem.find_by_title(data['title']):
                return {"msg": "Menu item with that title already exists."}, 400
            menu_item = MenuItem(**data)
            try:
                menu_item.save_to_db()
            except Exception as e:
                return {"msg": f"An error occurred while inserting the item.{e}"}, 500
            return {"msg": "Menu item is created successfully.", "menu_item": menu_item.json()}, 201
        return {"msg": "Тo access rights to perform this operation."}, 401

    @jwt_required(refresh=True)
    def put(self):
        data = request_parser('id', 'title', 'imageUrl', 'size', 'linkUrl').parse_args()
        menu_item = MenuItem.find_by_id(data['id'])

        if menu_item:
            if menu_item.title != data['title'] and MenuItem.find_by_title(data['title']):
                return {"msg": "Menu item with that title already exists."}, 400

            menu_item.title = data['title']
            menu_item.image_url = data['imageUrl']
            menu_item.size = data['size']
            menu_item.link_url = data['linkUrl']

            try:
                menu_item.save_to_db()
            except Exception as e:
                return {"msg": f"An error occurred while inserting the item.{e}"}, 500

            return {"msg": "Menu item was updated successfully.", "menu_item": menu_item.json()}, 200
        return {"msg": "Menu item with that id doesn't exists."}, 400


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
            response.append(menu.json_with_products(4))
        return response
