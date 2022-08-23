from modules.blocklist import Blocklist
from modules.users import UserModule
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required
)
from hmac import compare_digest
from datetime import datetime, timezone

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be left blank!"
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be left blank!"
                          )


class Register(Resource):
    def post(self):
        data = _user_parser.parse_args()
        if UserModule.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400
        UserModule(**data).save_to_db()
        return {"message": "User created successfully."}, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModule.find_by_username(data['username'])
        if user and compare_digest(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200
        return {'message': "Invalid credations"}


class UserLogout(Resource):
    @jwt_required()
    def post(cls):
        Blocklist(jti=get_jwt()["jti"], created_at=datetime.now(
            timezone.utc)).add_jti()
        return {"message": "Successfully logged out"}, 200


class User(Resource):
    @classmethod
    def get(cls, id: int):
        user = UserModule.find_by_id(id)
        if user:
            return user.json()
        return {'message': 'User Not Found'}, 404

    @classmethod
    def delete(cls, id: int):
        user = UserModule.find_by_id(id)
        if user:
            user.delete_from_db()
            return {'message': 'User deleted'}, 200
        return {'massage': 'User Not Found'}, 404


class Users(Resource):
    @classmethod
    def get(cls):
        users = UserModule.select_all()
        if users:
            return {'Users': [i.json() for i in users]}
        return {'massage': 'Users Not Found'}, 404


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        new_token = create_access_token(identity=user_id, fresh=True)
        return {
            'access_token': new_token
        }, 200
