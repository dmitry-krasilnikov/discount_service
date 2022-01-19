def brand_exists(cursor, brand_id):
    return (
        cursor.execute(
            "SELECT id FROM brand WHERE brand_id=? AND deleted_at IS NULL",
            (brand_id),
        ).fetchone()
        is not None
    )


def user_has_code_with_the_brand(cursor, user_id, brand_id):
    return (
        cursor.execute(
            "SELECT id FROM user_code "
            "LEFT JOIN brand_policy ON user_code.policy_id = brand_policy.id "
            "WHERE user_id=? AND brand_id=?",
            (user_id, brand_id),
        ).fetchone()
        is not None
    )


def select_policy_id(cursor, brand_id):
    row = cursor.execute(
        "SELECT id FROM brand_policy WHERE brand_id = ?",
        (brand_id,),
    ).fetchone()
    return None if row is None else row["id"]


def insert_user_code(cursor, user_id, brand_id, policy_id, code):
    return (
        cursor.execute(
            "insert into user_code (user_id, brand_id, policy_id, code) values (?, ?, ?, ?)",
            (user_id, brand_id, policy_id, code),
        ).fetchone()
        is not None
    )
