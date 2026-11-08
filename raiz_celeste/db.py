"""Una conexión por petición y consultas SQL con parámetros."""
from datetime import datetime
from decimal import Decimal

import mysql.connector
from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = mysql.connector.connect(
            host=current_app.config["MYSQL_HOST"],
            port=current_app.config["MYSQL_PORT"],
            user=current_app.config["MYSQL_USER"],
            password=current_app.config["MYSQL_PASSWORD"],
            database=current_app.config["MYSQL_DATABASE"],
            charset="utf8mb4", connection_timeout=5,
        )
    return g.db


def normalize(row):
    return {key: float(value) if isinstance(value, Decimal)
            else value.isoformat() if isinstance(value, datetime)
            else value for key, value in row.items()}


def query(sql, params=(), one=False):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        if one:
            return normalize(rows[0]) if rows else None
        return [normalize(row) for row in rows]
    finally:
        cursor.close()


def execute(sql, params=()):
    connection = get_db()
    cursor = connection.cursor()
    try:
        cursor.execute(sql, params)
        result = cursor.lastrowid
        connection.commit()
        return result
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()


def rollback():
    connection = g.get("db")
    if connection is not None and connection.is_connected():
        connection.rollback()


def close_db(error=None):
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


def init_app(app):
    app.teardown_appcontext(close_db)
