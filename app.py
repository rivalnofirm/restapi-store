import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError


from db import db
from ma import ma
from blacklist import BLACKLIST
from resources.user import User, UserRegister, UserLogin, UserLogout, TokenRefresh
from resources.item import Item, ItemList, NewItem, UpdateItem
from resources.store import Store, StoreList, NewStore


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = [
    "access",
    "refresh",
]
app.secret_key = "rival"

api = Api(app)
jwt = JWTManager(app)



@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


# API User
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(User, "/user/<int:user_id>")

# API Store
api.add_resource(NewStore, "/new-store/")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

# API Item
api.add_resource(NewItem, "/new-item/")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(UpdateItem, "/item-update/<int:id>")
api.add_resource(ItemList, "/items")


if __name__=='__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)