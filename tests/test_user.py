import unittest
import json
from db import db
from create_app import create_app


class UserTestCase(unittest.TestCase):
    """This class represents the user test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.test_user = json.dumps({
            "name": "maria",
            "email": "maria@maria.com",
            "password": 123,
            "confirmPassword": 123
        })

        # binds the app to the current context
        with self.app.app_context():
            db.create_all()

    def test_user_creation(self):
        """Test API can create a user (POST request)"""
        res = self.client.post('/user/register',
                               headers={"Content-Type": "application/json"},
                               data=self.test_user)
        self.assertEqual(res.status_code, 201)
        self.assertIn(b'"message": "User created successfully."', res.data)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
