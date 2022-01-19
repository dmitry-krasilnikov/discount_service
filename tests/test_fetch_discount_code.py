import re

from flask import url_for

import db


def test_able_to_get_discount_code(client):
    db.get_db().execute("INSERT INTO brand (admin_id, brand_id) VALUES (1, 2)")
    db.get_db().execute(
        "INSERT INTO brand_policy (brand_id, amount, count) VALUES (2, 10, 1)"
    )

    response = client.post(url_for("user.fetch_code"), json={"brandId": 2})

    assert response.status_code == 201
    assert response.mimetype == "application/json"
    payload = response.get_json()
    assert payload["result"] == "success"
    assert re.match(r"^[A-Z0-9]{20}$", payload["code"])

    code_records = (
        db.get_db()
        .execute("SELECT * FROM user_code WHERE code = ?", (payload["code"],))
        .fetchall()
    )
    assert len(code_records) == 1
    assert code_records[0]["brand_id"] == 2

    policy = (
        db.get_db().execute("SELECT * FROM brand_policy WHERE brand_id = 2").fetchone()
    )
    assert policy["issued"] == 1

    db.get_db().execute("DELETE FROM user_code")
    db.get_db().execute("DELETE FROM brand_policy")
    db.get_db().execute("DELETE FROM brand")

    # TODO test for event generation


def test_discount_codes_depleted(client):
    db.get_db().execute("INSERT INTO brand (admin_id, brand_id) VALUES (1, 2)")
    db.get_db().execute(
        "INSERT INTO brand_policy (brand_id, amount, count) VALUES (2, 10, 1)"
    )

    client.post(url_for("user.fetch_code"), json={"brandId": 2})
    response = client.post(url_for("user.fetch_code"), json={"brandId": 2})

    assert response.status_code == 403
    assert response.mimetype == "application/json"
    payload = response.get_json()
    assert payload["result"] == "error"
    assert payload["msg_id"] == "code_not_available"
    assert payload["msg"] == "The code is not available for this brand"

    db.get_db().execute("DELETE FROM user_code")
    db.get_db().execute("DELETE FROM brand_policy")
    db.get_db().execute("DELETE FROM brand")


def test_user_already_received_dicount_code(client):
    db.get_db().execute("INSERT INTO brand (admin_id, brand_id) VALUES (1, 2)")
    db.get_db().execute(
        "INSERT INTO brand_policy (brand_id, amount, count) VALUES (2, 10, 2)"
    )

    client.post(url_for("user.fetch_code"), json={"brandId": 2})
    response = client.post(url_for("user.fetch_code"), json={"brandId": 2})

    assert response.status_code == 403
    assert response.mimetype == "application/json"
    payload = response.get_json()
    assert payload["result"] == "error"
    assert payload["msg_id"] == "code_already_received"
    assert payload["msg"] == "User has already received a code"

    db.get_db().execute("DELETE FROM user_code")
    db.get_db().execute("DELETE FROM brand_policy")
    db.get_db().execute("DELETE FROM brand")


def test_db_consistency_on_user_already_received_code_error(client):
    db.get_db().execute("INSERT INTO brand (admin_id, brand_id) VALUES (1, 2)")
    db.get_db().execute(
        "INSERT INTO brand_policy (brand_id, amount, count) VALUES (2, 10, 2)"
    ).fetchone()

    client.post(url_for("user.fetch_code"), json={"brandId": 2})
    response = client.post(url_for("user.fetch_code"), json={"brandId": 2})

    payload = response.get_json()
    assert payload["msg_id"] == "code_already_received"

    issued = (
        db.get_db()
        .execute("SELECT issued FROM brand_policy WHERE brand_id = 2")
        .fetchone()["issued"]
    )
    assert issued == 1

    db.get_db().execute("DELETE FROM user_code")
    db.get_db().execute("DELETE FROM brand_policy")
    db.get_db().execute("DELETE FROM brand")


def test_brand_not_found(client):
    response = client.post(url_for("user.fetch_code"), json={"brandId": 2})

    assert response.status_code == 404
    assert response.mimetype == "application/json"
    payload = response.get_json()
    assert payload["result"] == "error"
    assert payload["msg_id"] == "brand_not_found"
    assert payload["msg"] == "Brand not found"
