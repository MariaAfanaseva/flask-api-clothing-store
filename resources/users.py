from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import User


def parse_user(*args):
    user_parser = reqparse.RequestParser()
    for arg in args:
        user_parser.add_argument(
            arg, type=str, required=True, help=f"{arg} field cannot be blank."
        )
    return user_parser


class UserRegister(Resource):
    def post(self):
        data = parse_user('name', 'email', 'password', 'confirmPassword').parse_args()

        if User.find_by_email(data['email']):
            return {"message": "A user with that email already exists."}, 400

        if data['password'] != data['confirmPassword']:
            return {"message": "The passwords mismatch"}, 400

        password = User.generate_hash(data['password'])
        user = User(name=data['name'], email=data['email'], password=password)
        user.save_to_db()
        return {"message": "User created successfully.", "user": user.json()}, 201


class UserLogin(Resource):
    def post(self):
        data = parse_user('email', 'password').parse_args()

        user = User.find_by_email(data['email'])

        if not user:
            return {"message": "User doesn't exist"}, 400

        elif user.verify_hash(data['password'], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": "Invalid credentials!"}, 401
