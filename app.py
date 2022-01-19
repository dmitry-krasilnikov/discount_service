from flask import Blueprint, Flask, Response


brand = Blueprint("brand", __name__, url_prefix="/brand")


@brand.route("/<int:brand_id>/policy", methods=["POST"])
def generate_codes(brand_id):
    return Response("", status=201)


def create_app():
    app = Flask(__name__)

    app.register_blueprint(brand)

    return app
