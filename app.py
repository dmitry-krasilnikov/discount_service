import os

from flask import Blueprint, Flask, Response, jsonify, request

import db
import queries
import service


# nice way to handle URL prefixes and allow for composition
brand = Blueprint("brand", __name__, url_prefix="/brand")
user = Blueprint("user", __name__, url_prefix="/user")

# TODO move to its own module
messages = {
    "brand_not_found": (404, "Brand not found"),
    "code_not_available": (403, "The code is not available for this brand"),
    "code_already_received": (403, "User has already received a code"),
}


@brand.route("/<int:brand_id>/policy", methods=["POST"])
def generate_codes(brand_id):
    payload = request.get_json()
    # some data is best validated in the controller before passing it to service layer
    # TODO refactor out into a validation layer
    if 1 > (amount := payload["amount"]) or amount > 100:
        return (
            jsonify(
                {
                    "result": "error",
                    "msg_id": "amount_invalid_range",
                    "msg": "Amount must be in range 1-100",
                }
            ),
            400,
        )
    if (count := payload["count"]) < 1:
        return (
            jsonify(
                {
                    "result": "error",
                    "msg_id": "count_invalid_range",
                    "msg": "Count must be a positive integer",
                }
            ),
            400,
        )

    success, result = service.generate_codes(brand_id, amount, count)

    # TODO refactor out common parts to make the code prettier and easier to read
    if success:
        return jsonify({"result": "success"}), 201
    elif result in messages:
        return (
            jsonify({"result": "error", "msg_id": result, "msg": messages[result][1]}),
            messages[result][0],
        )
    return jsonify({"result": "error", "msg_id": result, "msg": "Internal error"}), 500


@user.route("/codes", methods=["POST"])
def fetch_code():
    payload = request.get_json()
    # user_id must come from JWT of the user
    # for the purpose of this PoC it's hardcoded
    user_id = 1
    brand_id = payload["brandId"]

    # we avoid using exceptions here because they are quite slow
    # however that's not the only way of handling this
    # there's a nice pattern in Rust language with special Result class
    # which can help in such situations, especially when we consider
    # newly added patter matching capabilities
    success, result = service.get_code(user_id, brand_id)

    if success:
        return jsonify({"result": "success", "code": result}), 201
    elif result in messages:
        return (
            jsonify({"result": "error", "msg_id": result, "msg": messages[result][1]}),
            messages[result][0],
        )
    return jsonify({"result": "error", "msg_id": result, "msg": "Internal error"}), 500


def create_app(config_mapping=None):
    """App factory provides simple capabilites for testing"""
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
