from flask import url_for

import db


def test_50_codes_of_20_percent_discount_success(client):
    db.get_db().execute("INSERT INTO brand (admin_id, brand_id) VALUES (1, 3)")

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
