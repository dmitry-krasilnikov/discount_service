import secrets
import string

import queries


DISCOUNT_CODE_ALPHABET = string.ascii_uppercase + string.digits


def get_code(cursor, user_id, brand_id):
    code = "".join(secrets.choice(DISCOUNT_CODE_ALPHABET) for _ in range(20))
    policy_id = queries.select_policy_id(cursor, brand_id)
    if policy_id is None:
        return False, "brand_not_found"
    queries.insert_user_code(cursor, user_id, brand_id, policy_id, code)
    return True, code
