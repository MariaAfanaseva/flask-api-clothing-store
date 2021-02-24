import unittest
import json
from create_app import create_app
from fill_db import UpdateDb
from databases.db import db


class UserTestCase(unittest.TestCase):
    """This class represents the user test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app("testing")
        self.client = self.app.test_client()

        # binds the app to the current context
        with self.app.app_context():
            update = UpdateDb()
            update.clear_db()
            update.create_admin()

    def test_user_creation(self):
        """Test API can create a user (POST request)"""
        test_user = json.dumps(
            {
                "name": "maria",
                "email": "maria@maria.com",
                "password": 123,
                "confirmPassword": 123
            }
        )
        with self.client:
            res = self.client.post('/user/register',
                                   headers={"Content-Type": "application/json"},
                                   data=test_user)
            self.assertEqual(res.status_code, 201)
            self.assertIn(b'"msg": "User created successfully."', res.data)

    def test_create_incorrect_user(self):
        """Test API create user with mismatch passwords(POST request)"""
        test_user = json.dumps(
            {
                "name": "maria",
                "email": "maria@maria.com",
                "password": 123,
                "confirmPassword": 111
            }
        )
        with self.client:
            res = self.client.post('/user/register',
                                   headers={"Content-Type": "application/json"},
                                   data=test_user)
            self.assertEqual(res.status_code, 400)
            self.assertIn(b'"msg": "The passwords mismatch"', res.data)

    def test_create_user_without_confirm_password(self):
        """Test API create user without confirm password(POST request)"""
        test_user = json.dumps(
            {
                "name": "maria",
                "email": "maria@maria.com",
                "password": 123,
            }
        )
        with self.client:
            res = self.client.post('/user/register',
                                   headers={"Content-Type": "application/json"},
                                   data=test_user)
            self.assertEqual(res.status_code, 400)
            self.assertIn(b'"confirmPassword": "confirmPassword field cannot be blank."',
                          res.data)

    def test_create_user_with_blank_name(self):
        """Test API create user without name(POST request)"""
        test_user = json.dumps(
            {
                "email": "maria@maria.com",
                "password": 123,
                "confirmPassword": 123
            }
        )
        with self.client:
            res = self.client.post('/user/register',
                                   headers={"Content-Type": "application/json"},
                                   data=test_user)
            self.assertEqual(res.status_code, 400)
            self.assertIn(b'"name field cannot be blank."',
                          res.data)

    def test_user_creation_with_wrong_email(self):
        """Test API can create a user (POST request)"""
        test_user = json.dumps(
            {
                "name": "maria",
                "email": "@maria.com",
                "password": 123,
                "confirmPassword": 123
            }
        )
        with self.client:
            res = self.client.post('/user/register',
                                   headers={"Content-Type": "application/json"},
                                   data=test_user)
            self.assertEqual(res.status_code, 400)
            self.assertIn(b'"error": "There must be something before the @-sign."', res.data)

    def test_login_user(self):
        """Test API login user (POST request)"""
        test_user = json.dumps(
            {
                "email": "admin@admin.com",
                "password": "admin",
            }
        )
        with self.client:
            res = self.client.post('/user/login',
                                   headers={"Content-Type": "application/json"},
                                   data=test_user)
            self.assertEqual(res.status_code, 200)
            self.assertIn(b'"access_token"',
                          res.data)
            self.assertIn(b'"refresh_token"',
                          res.data)
            token = json.loads(res.data.decode())
            self.assertEqual(str, type(token['access_token']))
            self.refresh_token(token)
            self.logout(token)

    def logout(self, token):
        res_1 = self.client.post('/user/logout',
                                 headers={"Content-Type": "application/json",
                                          "Authorization": "Bearer " + token['access_token']},
                                 )
        self.assertEqual(res_1.status_code, 200)
        self.assertIn(b"User admin@admin.com successfully logged out.",
                      res_1.data)

        res_2 = self.client.post('/user/logout',
                                 headers={"Content-Type": "application/json",
                                          "Authorization": "Bearer " + token['access_token']},
                                 )
        self.assertEqual(res_2.status_code, 401)
        self.assertIn(b'"msg": "Token has been revoked"',
                      res_2.data)

    def refresh_token(self, token):
        res_1 = self.client.post('/user/refresh',
                                 headers={"Content-Type": "application/json",
                                        "Authorization": "Bearer " + token['refresh_token']},
                                 )
        self.assertEqual(res_1.status_code, 200)
        self.assertIn(b"access_token",
                      res_1.data)
        res_2 = self.client.post('/user/refresh',
                                 headers={"Content-Type": "application/json",
                                          "Authorization": "Bearer " + token['access_token']},
                                 )
        self.assertEqual(res_2.status_code, 422)
        self.assertIn(b'"msg": "Only refresh tokens are allowed"',
                      res_2.data)

    def test_login_user_without_password(self):
        """Test API login user without password(POST request)"""
        test_user = json.dumps(
            {
                "email": "admin@admin.com",
            }
        )
        with self.client:
            res = self.client.post('/user/login',
                                   headers={"Content-Type": "application/json"},
                                   data=test_user)
            self.assertEqual(res.status_code, 400)
            self.assertIn(b'"password field cannot be blank."',
                          res.data)

    def test_login_user_with_wrong_password(self):
        """Test API login user with wrong password(POST request)"""
        test_user = json.dumps(
            {
                "email": "admin@admin.com",
                "password": "a",
            }
        )
        with self.client:
            res = self.client.post('/user/login',
                                   headers={"Content-Type": "application/json"},
                                   data=test_user)
            self.assertEqual(res.status_code, 401)
            self.assertIn(b'"Invalid credentials!"',
                          res.data)

    def test_login_user_with_wrong_email(self):
        """Test API login user with wrong password(POST request)"""
        test_user = json.dumps(
            {
                "email": "a@a.com",
                "password": "a",
            }
        )
        with self.client:
            res = self.client.post('/user/login',
                                   headers={"Content-Type": "application/json"},
                                   data=test_user)
            self.assertEqual(res.status_code, 400)
            self.assertIn(b'"User doesn\'t exist"',
                          res.data)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
