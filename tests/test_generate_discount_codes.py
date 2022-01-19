from flask import url_for

import db


def test_create_policy(client):
    db.get_db().execute("INSERT INTO brand (admin_id, brand_id) VALUES (1, 3)")
    db.get_db().commit()

    response = client.post(
        url_for("brand.generate_codes", brand_id=3), json={"amount": 20, "count": 50}
    )

    assert response.status_code == 201
    assert response.mimetype == "application/json"
    assert response.get_json() == {"result": "success"}

    policies = db.get_db().execute("SELECT * FROM brand_policy").fetchall()

    assert len(policies) == 1
    assert policies[0]["brand_id"] == 3
    assert policies[0]["amount"] == 20
    assert policies[0]["count"] == 50

    db.get_db().execute("DELETE FROM brand_policy")
    db.get_db().execute("DELETE FROM brand")


def test_update_via_delete_and_create(client):
    db.get_db().execute("INSERT INTO brand (admin_id, brand_id) VALUES (1, 3)")

    client.post(
        url_for("brand.generate_codes", brand_id=3), json={"amount": 20, "count": 50}
    )
    response = client.post(
        url_for("brand.generate_codes", brand_id=3), json={"amount": 10, "count": 30}
    )

    assert response.status_code == 201
    assert response.mimetype == "application/json"
    assert response.get_json() == {"result": "success"}

    policies = db.get_db().execute("SELECT * FROM brand_policy ORDER BY id").fetchall()

    assert len(policies) == 2

    assert policies[0]["brand_id"] == 3
    assert policies[0]["amount"] == 20
    assert policies[0]["count"] == 50
    assert policies[0]["deleted_at"] is not None

    assert policies[1]["brand_id"] == 3
    assert policies[1]["amount"] == 10
    assert policies[1]["count"] == 30

    db.get_db().execute("DELETE FROM brand_policy")
    db.get_db().execute("DELETE FROM brand")


def test_brand_not_found(client):
    response = client.post(
        url_for("brand.generate_codes", brand_id=3), json={"amount": 20, "count": 50}
    )

    assert response.status_code == 404
    assert response.mimetype == "application/json"
    assert response.get_json() == {
        "result": "error",
        "msg_id": "brand_not_found",
        "msg": "Brand not found",
    }


def test_amount_is_less_than_allowed(client):
    db.get_db().execute("INSERT INTO brand (admin_id, brand_id) VALUES (1, 3)")

    response = client.post(
        url_for("brand.generate_codes", brand_id=3), json={"amount": 0, "count": 50}
    )

    assert response.status_code == 400
    assert response.mimetype == "application/json"
    assert response.get_json() == {
        "result": "error",
        "msg_id": "amount_invalid_range",
        "msg": "Amount must be in range 1-100",
    }


def test_amount_is_more_than_allowed(client):
    db.get_db().execute("INSERT INTO brand (admin_id, brand_id) VALUES (1, 3)")

    response = client.post(
        url_for("brand.generate_codes", brand_id=3), json={"amount": 101, "count": 50}
    )

    assert response.status_code == 400
    assert response.mimetype == "application/json"
    assert response.get_json() == {
        "result": "error",
        "msg_id": "amount_invalid_range",
        "msg": "Amount must be in range 1-100",
    }


def test_count_is_less_than_allowed(client):
    db.get_db().execute("INSERT INTO brand (admin_id, brand_id) VALUES (1, 3)")

    response = client.post(
        url_for("brand.generate_codes", brand_id=3), json={"amount": 15, "count": 0}
    )

    assert response.status_code == 400
    assert response.mimetype == "application/json"
    assert response.get_json() == {
        "result": "error",
        "msg_id": "count_invalid_range",
        "msg": "Count must be a positive integer",
    }
