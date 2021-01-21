from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, fresh_jwt_required
from models.item import ItemModel
from schemas.item import ItemSchema

NAME_ALREADY_EXISTS = "An item with name '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting the item."
ITEM_NOT_FOUND = "Item not found."
ITEM_DELETED = "Item deleted."

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class NewItem(Resource):
    @classmethod
    def post(cls):
        item_json = request.get_json()
        item = item_schema.load(item_json)

        if ItemModel.find_by_name(item.name):
            return {'message': NAME_ALREADY_EXISTS.format(item.name)}, 400
        
        try:
            item.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500

        return item_schema.dump(item), 201


class Item(Resource):
    @classmethod
    def get(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump(item), 200

        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    def delete(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": ITEM_DELETED}, 200

        return {"message": ITEM_NOT_FOUND}, 404


class ItemList(Resource):
    @classmethod
    def get(cls):
        return {"items": item_list_schema.dump(ItemModel.find_all())}, 200


class UpdateItem(Resource):
    @classmethod
    def patch(self, id: int):
        item = ItemModel.find_by_id(id)

        if (item):
            try:
                item.update_to_db(request.get_json())
            except:
                return {"message": ERROR_INSERTING}, 500
            return item_schema.dump(item), 200

    @classmethod
    def put(cls, id: int):
        item_json = request.get_json()
        item = ItemModel.find_by_id(id)

        if item:
            item.name = item_json["name"]
            item.description = item_json["description"]
            item.price = item_json["price"]
        else:
            item_json["id"] = id
            item = item_schema.load(item_json)

        item.save_to_db()

        return item_schema.dump(item), 200
