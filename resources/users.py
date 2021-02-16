from flask_restful import Resource, reqparse
from models.user import User


class UserRegister(Resource):
    def _parse_user(self):
        user_parser = reqparse.RequestParser()
        user_parser.add_argument(
            "name", type=str, required=True, help="Name field cannot be blank."
        )
        user_parser.add_argument(
            "email", type=str, required=True, help="Email field cannot be blank."
        )
        user_parser.add_argument(
            "password", type=str, required=True, help="Password field cannot be blank."
        )
        user_parser.add_argument(
            "confirmPassword", type=str, required=True, help="Confirm password field cannot be blank."
        )
        return user_parser

    def post(self):
        data = self._parse_user().parse_args()

        if User.find_by_email(data['email']):
            return {"message": "A user with that email already exists."}, 400

        if data['password'] != data['confirmPassword']:
            return {"message": "The passwords mismatch"}, 400

        user = User(name=data['name'], email=data['email'], password=data['password'])
        user.save_to_db()
        return {"message": "User created successfully.", "user": user.json()}, 201
