import json
from models.menu_item import MenuItem, Product
from models.user import User
from db import db


class UpdateDb:
    def _clear_db(self):
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

    def create_admin(self):
        admin = User(name='admin', email='admin@admin.com', password='admin', is_admin=True)
        admin.save_to_db()

    def recreate_db(self):
        self._clear_db()
        self.fill_menu()
        self.fill_products()
        self.create_admin()
