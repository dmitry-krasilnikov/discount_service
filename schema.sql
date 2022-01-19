PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS user_code;
DROP TABLE IF EXISTS brand_policy;
DROP TABLE IF EXISTS brand;
-- DROP TABLE IF EXISTS brand_admin;

-- -- TODO leave only 2 tables
-- -- TODO figure out how to increment issued properly
-- CREATE TABLE brand_admin (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   admin_id INTEGER UNIQUE NOT NULL,
--   deleted_at TIMESTAMP
-- );

CREATE TABLE brand (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  admin_id INTEGER UNIQUE NOT NULL,
  brand_id INTEGER UNIQUE NOT NULL,
  deleted_at TIMESTAMP
);

CREATE TABLE brand_policy (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  brand_id INTEGER UNIQUE NOT NULL,
  amount INTEGER NOT NULL,
  count INTEGER NOT NULL,
  issued INTEGER NOT NULL DEFAULT 0 CHECK(issued <= count),
  deleted_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (brand_id) REFERENCES brand (brand_id)
);

CREATE TABLE user_code (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  brand_id INTEGER NOT NULL,
  policy_id INTEGER NOT NULL,
  code TEXT UNIQUE NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  redeemed_at TIMESTAMP,
  UNIQUE (user_id, brand_id),
  FOREIGN KEY (policy_id) REFERENCES brand_policy (id),
  FOREIGN KEY (brand_id) REFERENCES brand (brand_id)
);

-- INSERT INTO brand_admin (admin_id) VALUES (1);
-- INSERT INTO brand (admin_id, brand_id) VALUES (1, 2);
