from flask import url_for


def test_50_codes_of_20_percent_discount_success(client):
    response = client.post(url_for("brand.generate_codes", brand_id=1))

    assert response.status_code == 201
