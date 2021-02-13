import json
from models.menu_items import MenuItemsModel
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
            item = MenuItemsModel(**data)
            item.save_to_db()

    def recreate_db(self):
        self._clear_db()
        self.fill_menu()
