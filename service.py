"""Service layer functions containg DB queries' calls.

Most of the 'logic' has been shifted to the DB level because it's simple.
If there were more business rules then it would make sense
to break the service layer further.
"""

import secrets
import string

import sqlite3

import db
import queries


DISCOUNT_CODE_ALPHABET = string.ascii_uppercase + string.digits


def generate_codes(brand_id: int, amount: int, count: int):
    queries.delete_active_policies(brand_id)
    try:
        queries.insert_policy(brand_id, amount, count)
    except sqlite3.IntegrityError as exc:
        if "FOREIGN KEY constraint failed" in str(exc):
            return False, "brand_not_found"
        raise
    db.get_db().commit()
    return True, "success"


def get_code(user_id, brand_id):
    code = "".join(secrets.choice(DISCOUNT_CODE_ALPHABET) for _ in range(20))

    policy_id = queries.select_policy_id(brand_id)
    if policy_id is None:
        return False, "brand_not_found"
    try:
        queries.increment_issued(policy_id)
    except sqlite3.IntegrityError as exc:
        if "CHECK constraint failed: issued <= count" in str(exc):
            return False, "code_not_available"
        raise
    try:
        queries.insert_user_code(user_id, brand_id, policy_id, code)
    except sqlite3.IntegrityError as exc:
        if "UNIQUE constraint failed: user_code.user_id, user_code.brand_id" in str(
            exc
        ):
            db.get_db().rollback()
            return False, "code_already_received"
        raise
    # sqlite3 starts transaction automatically for any state changing query
    db.get_db().commit()
    return True, code
