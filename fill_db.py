import json
from models.menu_items import MenuItemsModel


class FillDb:
    def _read_file(self, file_name):
        with open(f'json_files/{file_name}', 'r') as file:
            menu_items = json.load(file)
            return menu_items

    def fill_menu(self):
        menu_items = self._read_file('menu.json')
        for data in menu_items:
            item = MenuItemsModel(**data)
            item.save_to_db()


if __name__ == '__main__':
    create_data = FillDb()
    create_data.fill_menu()
