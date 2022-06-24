from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.users import Register, User, Users, UserLogin, UserLogout, TokenRefresh
from resources.items import Item, Items
from resources.store import Store, StoreList
from resources.greeting import Greeting
from modules.blocklist import Blocklist

from datetime import timedelta
import os

try:
    uri = os.getenv("DATABASE_URL")  # or other relevant config var
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
except:
    pass

app = Flask(__name__)
app.secret_key = "skdnmlcnevnle332d2"
app.config['JWT_SECRET_KEY'] = "fdsfkds;33wejvk3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = uri if uri else 'sqlite:///mydata.db'
jwt = JWTManager(app)


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'admin': True}
    else:
        return {'admin': False}


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    return Blocklist.find_by_jti(jwt_payload["jti"]) is not None


@jwt.expired_token_loader
def expired_callback():
    return jsonify({
        "massage": "The token has expired"
    }), 401


@jwt.invalid_token_loader
def invalid_callback(err):
    return jsonify({
        "massage": "The token is invalid",
        "err": err
    }), 401


@jwt.unauthorized_loader
def unauthorized_callback():
    return jsonify({
        "massage": "The token unauthorized"
    }), 401


@jwt.needs_fresh_token_loader
def fresh_callback():
    return jsonify({
        "massage": "The token have to be freshed"
    }), 401


@jwt.revoked_token_loader
def revoked_callback():
    return jsonify({
        "massage": "The token has revoked"
    }), 401


api = Api(app)

api.add_resource(Greeting, "/")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(Items, "/items")
api.add_resource(Register, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(User, "/user/<int:id>")
api.add_resource(Users, "/users")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run()
