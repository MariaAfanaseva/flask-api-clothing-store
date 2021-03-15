import unittest
import json
from databases.db import db
from create_app import create_app
from fill_db import UpdateDb
from tests.users import ADMIN_USER, USER


class ItemsTestCase(unittest.TestCase):
    """This class represents the product items test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.test_admin = json.dumps(ADMIN_USER)
        self.test_user = json.dumps(USER)
        self.test_product = dict({
            "name": "Blue Hat",
            "imageUrl": "/images/shop-img/hats/blue-beanie.png",
            "price": 25,
            "menuTitles": ["hats", "womens", "mens"]
        })

        with self.app_context:
            update = UpdateDb()
            update.recreate_db()

    def login_user(self, test_user):
        res = self.client.post('/user/login',
                               headers={"Content-Type": "application/json"},
                               data=test_user)
        token = json.loads(res.data.decode())
        return token

    def test_menu_products(self):
        """Test API can get a shop items (GET request)"""
        with self.app_context:
            res = self.client.get('/shop/hats')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(list, type(res.json['products']))

    def test_create_product(self):
        """Test API can create a new product (POST request)"""
        with self.app_context:
            token = self.login_user(self.test_admin)
            res = self.client.post('/product',
                                   headers={"Content-Type": "application/json",
                                            "Authorization": "Bearer " + token['refresh_token']},
                                   data=json.dumps(self.test_product)
                                   )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 201)
            self.assertEqual("Product is created successfully.",
                             data['msg'])

    def test_shop_products(self):
        """Test API can get a shop (GET request)"""
        with self.app_context:
            res = self.client.get('/shop')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(list, type(res.json))
            self.assertEqual(4, len(res.json[0]['items']))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app_context:
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
