import json
import os
from models.menu_item import MenuItem, Product
from models.user import User
from databases.db import db
from create_app import create_app
from dotenv import load_dotenv

load_dotenv('configs/.env-users')


class UpdateDb:
    def clear_db(self):
        db.drop_all()
        db.create_all()

    def _read_file(self, file_name):
        with open(f'json_files/{file_name}', 'r') as file:
            menu_items = json.load(file)
            return menu_items

    def fill_menu(self):
        menu_items = self._read_file('menu.json')
        for data in menu_items:
            item = MenuItem(**data)
            item.save_to_db()

    def fill_products(self):
        products = self._read_file('products.json')
        for data in products:
            product = Product(name=data['name'], image_url=data['imageUrl'],
                              price=data['price'])
            product.save_to_db()
            for title in data['menuTitles']:
                menu = MenuItem.find_by_title(title)
                menu.products.append(product)
                menu.save_to_db()

    @staticmethod
    def create_admin():
        admin = User(name=os.getenv('ADMIN_NAME'), email=os.getenv('ADMIN_EMAIL'),
                     password=os.getenv('ADMIN_PASSWORD'), is_admin=True)
        admin.save_to_db()

    @staticmethod
    def create_user():
        user = User(name=os.getenv('USER_NAME'), email=os.getenv('USER_EMAIL'),
                    password=os.getenv('USER_PASSWORD'))
        user.save_to_db()

    def recreate_db(self):
        self.clear_db()
        self.fill_menu()
        self.fill_products()
        self.create_admin()
        self.create_user()


if __name__ == '__main__':
    app = create_app("development")
    with app.app_context():
        update = UpdateDb()
        update.recreate_db()
