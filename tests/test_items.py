import unittest
from databases.db import db
from create_app import create_app
from fill_db import UpdateDb


class ItemsTestCase(unittest.TestCase):
    """This class represents the product items test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app("testing")
        self.client = self.app.test_client()

        with self.app.app_context():
            update = UpdateDb()
            update.recreate_db()

    def test_menu_products(self):
        """Test API can get a shop items (GET request)"""
        res = self.client.get('/shop/hats')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list, type(res.json['products']))

    def test_shop_products(self):
        """Test API can get a shop (GET request)"""
        res = self.client.get('/shop')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list, type(res.json))
        self.assertEqual(4, len(res.json[0]['items']))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
