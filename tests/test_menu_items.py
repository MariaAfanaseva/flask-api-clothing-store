import json
import unittest
from databases.db import db
from create_app import create_app
from fill_db import UpdateDb
from tests.users import ADMIN_USER, USER
from models.menu_item import MenuItem


class MenuItemsTestCase(unittest.TestCase):
    """This class represents the menu items test case."""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.test_menu_item = json.dumps(
            {
                "title": "Dress",
                "imageUrl": "images/dress",
                "size": "",
                "linkUrl": "shop/dress",
            }
        )
        self.existed_menu_item = json.dumps(
            {
                "title": "hats",
                "imageUrl": "images/hats",
                "size": "",
                "linkUrl": "shop/hats",
            }
        )
        self.updated_menu_item = {
                "id": 1,
                "title": "hats",
                "imageUrl": "images/hats",
                "size": "large",
                "linkUrl": "shop/hats",
            }

        self.test_admin = json.dumps(ADMIN_USER)
        self.test_user = json.dumps(USER)

        with self.app_context:
            update = UpdateDb()
            update.recreate_db()

    def test_menu_items(self):
        """Test API can get a menu items (GET request)."""
        with self.app_context:
            res = self.client.get('/menu')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(list, type(res.json['menuItems']))

    def login_user(self, test_user):
        res = self.client.post('/user/login',
                               headers={"Content-Type": "application/json"},
                               data=test_user)
        token = json.loads(res.data.decode())
        return token

    def test_create_menu_item(self):
        """Test API can create a menu item (POST request)."""
        with self.app_context:
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
        """Test API can not create a menu item with access token
        instead refresh token (POST request)
        """
        with self.app_context:
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
        """Test API can not create a menu item
        with not admin user (POST request)
        """
        with self.app_context:
            token = self.login_user(self.test_user)
            res = self.client.post('/menu',
                                   headers={"Content-Type": "application/json",
                                            "Authorization": "Bearer " + token['refresh_token']},
                                   data=self.test_menu_item
                                   )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 401)
            self.assertEqual('Admin privilege required.',
                             data['msg'])

    def test_create_menu_item_with_wrong_data(self):
        """Test API can not create a menu item
        with the wrong data(POST request)
        """
        with self.app_context:
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

    def test_create_menu_item_with_existed_title(self):
        """Test API can not create a menu item with title,
        that already exists (POST request)
        """
        with self.app_context:
            token = self.login_user(self.test_admin)
            res = self.client.post('/menu',
                                   headers={"Content-Type": "application/json",
                                            "Authorization": "Bearer " + token['refresh_token']},
                                   data=self.existed_menu_item
                                   )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertEqual('Menu item with that title already exists.',
                             data['msg'])

    def test_update_menu_item(self):
        """Test API can update a menu item (PUT request)."""
        with self.app_context:
            token = self.login_user(self.test_admin)
            res = self.client.put('/menu',
                                  headers={"Content-Type": "application/json",
                                           "Authorization": "Bearer " + token['refresh_token']},
                                  data=json.dumps(self.updated_menu_item)
                                  )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 200)
            self.assertEqual('Menu item was updated successfully.',
                             data['msg'])
            self.assertEqual('large',
                             data['menu_item']['size'])

    def test_update_menu_item_with_wrong_id(self):
        """Test API can not update a menu item with wrong id (PUT request)."""
        with self.app_context:
            menu_item = self.updated_menu_item.copy()
            menu_item['id'] = 'sdf'
            token = self.login_user(self.test_admin)
            res = self.client.put('/menu',
                                  headers={"Content-Type": "application/json",
                                           "Authorization": "Bearer " + token['refresh_token']},
                                  data=json.dumps(menu_item)
                                  )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertEqual('id field must be integer.',
                             data['message']['id'])

    def test_update_menu_item_with_wrong_title(self):
        """Test API can not update a menu item title, that already exists (PUT request)."""
        with self.app_context:
            menu_item = self.updated_menu_item.copy()
            menu_item['title'] = 'jackets'
            token = self.login_user(self.test_admin)
            res = self.client.put('/menu',
                                  headers={"Content-Type": "application/json",
                                           "Authorization": "Bearer " + token['refresh_token']},
                                  data=json.dumps(menu_item)
                                  )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertEqual('Menu item with that title already exists.',
                             data['msg'])

    def test_update_menu_item_with_wrong_user(self):
        """Test API can not update a menu item
        with a user who is not admin (PUT request).
        """
        with self.app_context:
            token = self.login_user(self.test_user)
            res = self.client.put('/menu',
                                  headers={"Content-Type": "application/json",
                                           "Authorization": "Bearer " + token['refresh_token']},
                                  data=json.dumps(self.updated_menu_item)
                                  )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 401)
            self.assertEqual('Admin privilege required.',
                             data['msg'])

    def test_delete_menu_item(self):
        """Test API can delete a menu item (DELETE request)."""
        with self.app_context:
            token = self.login_user(self.test_admin)
            res = self.client.delete('/menu',
                                     headers={"Content-Type": "application/json",
                                              "Authorization": "Bearer " + token['refresh_token']},
                                     data=json.dumps({"id": 1})
                                     )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 200)
            self.assertEqual('Menu item was deleted successfully.',
                             data['msg'])

            data = MenuItem.find_by_id(1)
            self.assertEqual(data, None)

    def test_delete_menu_item_with_wrong_user(self):
        """Test API can not delete a menu item
        with a user who is not admin (DELETE request).
        """
        with self.app_context:
            token = self.login_user(self.test_user)
            res = self.client.delete('/menu',
                                     headers={"Content-Type": "application/json",
                                              "Authorization": "Bearer " + token['refresh_token']},
                                     data=json.dumps({"id": 1})
                                     )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 401)
            self.assertEqual('Admin privilege required.',
                             data['msg'])

    def test_delete_menu_item_with_wrong_token(self):
        """Test API can not delete a menu item
        with access token instead refresh token (DELETE request).
        """
        with self.app_context:
            token = self.login_user(self.test_admin)
            res = self.client.delete('/menu',
                                     headers={"Content-Type": "application/json",
                                              "Authorization": "Bearer " + token['access_token']},
                                     data=json.dumps({"id": 1})
                                     )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 422)
            self.assertEqual('Only refresh tokens are allowed',
                             data['msg'])

    def test_delete_menu_item_with_wrong_id(self):
        """Test API can not delete a menu item
        with id that doesn't exists (DELETE request).
        """
        with self.app_context:
            token = self.login_user(self.test_admin)
            res = self.client.delete('/menu',
                                     headers={"Content-Type": "application/json",
                                              "Authorization": "Bearer " + token['refresh_token']},
                                     data=json.dumps({"id": 10})
                                     )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertEqual("Menu item with that id doesn't exists.",
                             data['msg'])

    def test_delete_menu_item_with_wrong_data(self):
        """Test API can not delete a menu item
        without id(DELETE request).
        """
        with self.app_context:
            token = self.login_user(self.test_admin)
            res = self.client.delete('/menu',
                                     headers={"Content-Type": "application/json",
                                              "Authorization": "Bearer " + token['refresh_token']},
                                     data=json.dumps({"title": "hats"})
                                     )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertEqual("id field must be integer.",
                             data['message']['id'])

    def tearDown(self):
        """Teardown all initialized variables."""
        with self.app_context:
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
