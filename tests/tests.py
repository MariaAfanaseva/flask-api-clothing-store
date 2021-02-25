import unittest
from tests.test_user import UserTestCase
from tests.test_items import ItemsTestCase
from tests.test_menu_items import MenuItemsTestCase

if __name__ == "__main__":
    user = unittest.TestLoader().loadTestsFromModule(UserTestCase)
    items = unittest.TestLoader().loadTestsFromModule(ItemsTestCase)
    menu_items = unittest.TestLoader().loadTestsFromModule(MenuItemsTestCase)
    unittest.TextTestRunner(verbosity=2).run(user)
    unittest.TextTestRunner(verbosity=2).run(items)
    unittest.TextTestRunner(verbosity=2).run(menu_items)
