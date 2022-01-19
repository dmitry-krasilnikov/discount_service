import os

from flask import Blueprint, Flask, Response, jsonify, request

import db
import queries
import service


brand = Blueprint("brand", __name__, url_prefix="/brand")
user = Blueprint("user", __name__, url_prefix="/user")


@brand.route("/<int:brand_id>/policy", methods=["POST"])
def generate_codes(brand_id):
    payload = request.get_json()
    amount = payload["amount"]
    count = payload["count"]

    cursor = db.get_db().cursor()
    cursor.execute(
        "INSERT INTO brand_policy (brand_id, amount, count) VALUES (?, ?, ?)",
        (brand_id, amount, count),
    )

    return jsonify({"result": "success"}), 201


@user.route("/codes", methods=["POST"])
def fetch_code():
    payload = request.get_json()
    user_id = 1
    brand_id = payload["brandId"]

    cursor = db.get_db().cursor()
    success, result = service.get_code(cursor, user_id, brand_id)

    if success:
        return jsonify({"result": "success", "code": result}), 201
    return jsonify({"result": "error", "msg_id": result}), 500


def create_app(config_mapping=None):
    app = Flask(__name__)

    default_config_mapping = {
        "SECRET_KEY": "dev",
        "DATABASE": os.path.join(app.instance_path, "discount_service.sqlite"),
    }
    default_config_mapping.update(config_mapping)
    app.config.from_mapping(**default_config_mapping)

    app.register_blueprint(brand)
    app.register_blueprint(user)

    db.init_app(app)

    return app
