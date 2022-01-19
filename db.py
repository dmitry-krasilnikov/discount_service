import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if "db" not in g:
        # g.db is a request level context which is usually used for storing such data
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Row class provides a nice 'dict' like interface to manipulate data
        g.db.row_factory = sqlite3.Row

    # enable foreign key constraints because we rely on them in our business logic
    g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


def load_data():
    db = get_db()

    db.execute("INSERT INTO brand (admin_id, brand_id) VALUES (1, 1)")
    db.commit()


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


@click.command("load-data")
@with_appcontext
def load_data_command():
    """Load minimal data for manual local testing."""
    load_data()
    click.echo("Loaded data.")


def init_app(app):
    # automatically close DB connection when the app stops
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(load_data_command)
