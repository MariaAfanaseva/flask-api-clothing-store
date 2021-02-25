import json
import unittest
from databases.db import db
from create_app import create_app
from fill_db import UpdateDb
from tests.users import ADMIN_USER, USER


class MenuItemsTestCase(unittest.TestCase):
    """This class represents the menu items test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.test_menu_item = json.dumps(
            {
                "title": "Dress",
                "imageUrl": "images/dress",
                "size": "",
                "linkUrl": "shop/dress",
            }
        )
        self.test_admin = json.dumps(ADMIN_USER)
        self.test_user = json.dumps(USER)

        with self.app.app_context():
            update = UpdateDb()
            update.recreate_db()

    def test_menu_items(self):

        """Test API can get a menu items (GET request)"""

        res = self.client.get('/menu')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(list, type(res.json['menuItems']))

    def login_user(self, test_user):
        with self.client:
            res = self.client.post('/user/login',
                                   headers={"Content-Type": "application/json"},
                                   data=test_user)
            token = json.loads(res.data.decode())
            return token

    def test_create_menu_item(self):

        """Test API can create a menu item (POST request)"""

        token = self.login_user(self.test_admin)
        res = self.client.post('/menu',
                               headers={"Content-Type": "application/json",
                                        "Authorization": "Bearer " + token['refresh_token']},
                               data=self.test_menu_item
                               )
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 201)
        self.assertEqual('Menu item is created successfully.',
                         data['msg'])

    def test_create_menu_item_with_wrong_token(self):

        """Test API can create a menu item with access token instead refresh token (POST request)"""

        token = self.login_user(self.test_admin)
        res = self.client.post('/menu',
                               headers={"Content-Type": "application/json",
                                        "Authorization": "Bearer " + token['access_token']},
                               data=self.test_menu_item
                               )
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 422)
        self.assertEqual('Only refresh tokens are allowed',
                         data['msg'])

    def test_create_menu_item_with_wrong_user(self):

        """Test API can create a menu item with not admin user (POST request)"""

        token = self.login_user(self.test_user)
        res = self.client.post('/menu',
                               headers={"Content-Type": "application/json",
                                        "Authorization": "Bearer " + token['refresh_token']},
                               data=self.test_menu_item
                               )
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual('Тo access rights to perform this operation.',
                         data['msg'])

    def test_create_menu_item_with_wrong_data(self):

        """Test API can create a menu item with wrong data(POST request)"""

        test_menu_item = json.dumps({"title": "Dress"})
        token = self.login_user(self.test_admin)
        res = self.client.post('/menu',
                               headers={"Content-Type": "application/json",
                                        "Authorization": "Bearer " + token['refresh_token']},
                               data=test_menu_item
                               )
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual('imageUrl field cannot be blank.',
                         data['message']['imageUrl'])

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
