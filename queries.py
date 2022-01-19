"""DB query layer.

If there's a need to switch DB back-ends often ORM can help to abstract from DB access.
For most simple cases raw SQL can be sufficient and easy to understand.
"""
import db


def delete_active_policies(brand_id):
    db.get_db().execute(
        "UPDATE brand_policy SET deleted_at = DATETIME('now') WHERE brand_id = ? AND deleted_at IS NULL",
        (brand_id,),
    )


def insert_policy(brand_id, amount, count):
    db.get_db().execute(
        "INSERT INTO brand_policy (brand_id, amount, count) VALUES (?, ?, ?)",
        (brand_id, amount, count),
    )


def select_policy_id(brand_id):
    row = (
        db.get_db()
        .execute(
            "SELECT id FROM brand_policy WHERE brand_id = ?",
            (brand_id,),
        )
        .fetchone()
    )
    return None if row is None else row["id"]


def increment_issued(policy_id):
    db.get_db().execute(
        "update brand_policy set issued = issued + 1 where id = ?",
        (policy_id,),
    )


def insert_user_code(user_id, brand_id, policy_id, code):
    return (
        db.get_db()
        .execute(
            "insert into user_code (user_id, brand_id, policy_id, code) values (?, ?, ?, ?)",
            (user_id, brand_id, policy_id, code),
        )
        .fetchone()
        is not None
    )
