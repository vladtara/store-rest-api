from modules.users import UserModule
from flask_restful import Resource, reqparse


class Register(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = Register.parser.parse_args()
        if UserModule.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400
        UserModule(**data).save_to_db()
        return {"message": "User created successfully."}, 201


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
