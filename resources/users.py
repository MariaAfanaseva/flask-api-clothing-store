from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                get_jwt,
                                get_jwt_identity)
from models.user import User
from databases.redis_db import is_jti_blocklisted, add_jti_token


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
            return {"msg": "A user with that email already exists."}, 400

        if data['password'] != data['confirmPassword']:
            return {"msg": "The passwords mismatch"}, 400

        user = User(name=data['name'], email=data['email'], password=data['password'])
        user.save_to_db()
        return {"msg": "User created successfully.", "user": user.json()}, 201


class UserLogin(Resource):
    def post(self):
        data = parse_user('email', 'password').parse_args()

        user = User.find_by_email(data['email'])

        if not user:
            return {"msg": "User doesn't exist"}, 400

        elif user.verify_password(data['password']):
            access_token = create_access_token(identity=user.email, fresh=True)
            refresh_token = create_refresh_token(user.email)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"msg": "Invalid credentials!"}, 401


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_email = get_jwt_identity()

        if not is_jti_blocklisted(jti):
            add_jti_token(jti)
            return {"msg": f"User {user_email} successfully logged out."}, 200


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
