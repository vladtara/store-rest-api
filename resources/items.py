from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from modules.items import ItemModule
from typing import *


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True,
                        help="This field cannot be left blank!")
    parser.add_argument("store_id", type=float, required=True,
                        help="This field must have store id!")

    def get(self, name: str):
        item = ItemModule.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required(fresh=True)
    def post(self, name: str):
        if ItemModule.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
        else:
            data = Item.parser.parse_args()
            item = ItemModule(name, **data)
            try:
                item.save_to_db()
            except:
                return {"message": "An error occurred inserting the item."}, 500
            return item.json(), 201

    @jwt_required()
    def put(self, name: str):
        data = Item.parser.parse_args()
        item = ItemModule.find_by_name(name)
        if item:
            try:
                item.price = data["price"]
                item.store_id = data["store_id"]
                item.save_to_db()
            except:
                return {"message": "An error occurred updating the item."}, 500
            return {'message': "An item with name '{}' is updated.".format(name)}, 201
        else:
            try:
                item = ItemModule(name, **data)
                item.save_to_db()

            except:
                return {"message": "An error occurred inserting the item."}, 500
            return {'message': "An item with name '{}' is created.".format(name)}, 201

    @jwt_required()
    def delete(self, name: str):
        item = ItemModule.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': "An item with name '{}' is deleted.".format(name)}, 200
        else:
            return {'message': "An item with name '{}' not exist.".format(name)}, 404


class Items(Resource):
    def get(self):
        items = [item.json() for item in ItemModule.select_all()]
        return {'items': items}, 200
