from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from models.menu_item import MenuItem
from models.product import Product
from models.user import User


def request_parser(*args):
    parser = reqparse.RequestParser()
    for arg in args:
        if arg == 'id':
            parser.add_argument(
                arg, type=int, required=True, help="id field must be integer."
            )
        elif arg == 'menuTitles':
            parser.add_argument(
                arg, type=str, required=True, help="menuTitles field must be list.",
                action='append'
            )
        elif arg == 'price':
            parser.add_argument(
                arg, type=float, required=True, help="price field must be float."
            )
        else:
            parser.add_argument(
                arg, type=str, required=True, help=f"{arg} field cannot be blank."
            )
    return parser


class Products(Resource):
    def get(self, title):
        products = MenuItem.query.filter_by(title=title).first().products
        if products:
            return {"products": [x.json() for x in products]}
        else:
            return {'error': 'Not found'}


class UpdateProduct(Resource):
    @jwt_required(refresh=True)
    def post(self):
        user_email = get_jwt_identity()
        if User.find_by_email(user_email).is_admin:
            data = request_parser('name', 'imageUrl', 'price', 'menuTitles').parse_args()
            product = Product(name=data['name'], image_url=data['imageUrl'],
                              price=data['price'])
            try:
                product.save_to_db()
                for title in data['menuTitles']:
                    menu = MenuItem.find_by_title(title)
                    menu.products.append(product)
                    menu.save_to_db()
            except Exception as e:
                return {"msg": f"An error occurred while inserting the item.{e}"}, 500
            return {"msg": "Product is created successfully.", "menu_item": product.json()}, 201
        return {"msg": "Admin privilege required."}, 401
