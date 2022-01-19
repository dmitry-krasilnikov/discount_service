import re

from flask import url_for

import db


def test_get_discount_code_from_brand_success(client):
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

    db.get_db().execute("DELETE FROM user_code")
    db.get_db().execute("DELETE FROM brand_policy")
    db.get_db().execute("DELETE FROM brand")

    # TODO test for event generation
