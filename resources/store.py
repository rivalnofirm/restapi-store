from flask_restful import Resource
from flask import request
from models.store import StoreModel
from schemas.store import StoreSchema

NAME_ALREADY_EXISTS = "A store with name '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting the store."
STORE_NOT_FOUND = "Store not found."
STORE_DELETED = "Store deleted."

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)


class NewStore(Resource):
    @classmethod
    def post(cls):
        store_json = request.get_json()
        store = store_schema.load(store_json)

        if StoreModel.find_by_name(store.name):
            return {'message': NAME_ALREADY_EXISTS.format(store.name)}, 400
        
        try:
            store.save_to_db()
        except:
            return {'message': ERROR_INSERTING}, 500

        return store_schema.dump(store), 201


class Store(Resource):
    @classmethod
    def get(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return store_schema.dump(store), 200

        return {"message": STORE_NOT_FOUND}, 404


    @classmethod
    def delete(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": STORE_DELETED}, 200

        return {"message": STORE_NOT_FOUND}, 404


class StoreList(Resource):
    @classmethod
    def get(cls):
        return {"stores": store_list_schema.dump(StoreModel.find_all())}, 200