from decimal import Decimal, InvalidOperation
from urllib.parse import urlsplit

from flask import Blueprint, abort, jsonify, request

from . import db

api = Blueprint("api", __name__)
PLANT_SELECT = """SELECT p.*, c.nombre AS categoria
                  FROM plantas p JOIN categorias c ON c.id = p.categoria_id"""
PLANT_FIELDS = ("categoria_id", "nombre", "nombre_cientifico", "descripcion",
                "precio", "stock", "imagen", "luz", "riego", "destacada")


def body():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValueError("Enviá un objeto JSON válido.")
    return data


def text(data, name, limit, required=False):
    value = data.get(name, "")
    if not isinstance(value, str):
        raise ValueError(f"{name}: debe ser un texto.")
    value = value.strip()
    if required and not value:
        raise ValueError(f"{name}: es obligatorio.")
    if len(value) > limit:
        raise ValueError(f"{name}: máximo {limit} caracteres.")
    return value


def integer(data, name, minimum=0):
    value = data.get(name)
    if isinstance(value, bool) or not isinstance(value, int) or not minimum <= value <= 2147483647:
        raise ValueError(f"{name}: debe ser un entero entre {minimum} y 2147483647.")
    return value


def validate_plant(data):
    result = {
        "categoria_id": integer(data, "categoria_id", 1),
        "nombre": text(data, "nombre", 100, True),
        "nombre_cientifico": text(data, "nombre_cientifico", 150),
        "descripcion": text(data, "descripcion", 5000, True),
        "stock": integer(data, "stock"),
        "imagen": text(data, "imagen", 255),
        "luz": text(data, "luz", 100),
        "riego": text(data, "riego", 150),
    }
    try:
        price = Decimal(str(data.get("precio")))
        if not price.is_finite() or not Decimal("0") < price <= Decimal("99999999.99"):
            raise ValueError
        if price != price.quantize(Decimal("0.01")):
            raise ValueError
    except (InvalidOperation, ValueError):
        raise ValueError("precio: ingresá un valor positivo con hasta dos decimales.") from None
    result["precio"] = price
    featured = data.get("destacada", False)
    if not isinstance(featured, bool):
        raise ValueError("destacada: debe ser verdadero o falso.")
    result["destacada"] = featured
    image = result["imagen"]
    if image and not (image.startswith("/static/img/") or
                      (urlsplit(image).scheme in ("http", "https") and urlsplit(image).netloc)):
        raise ValueError("imagen: usá una ruta /static/img/ o una URL http/https.")
    return result


@api.errorhandler(ValueError)
def invalid_data(error):
    return jsonify(error=str(error)), 400


@api.get("/plantas")
def list_plants():
    clauses, values = [], []
    search = request.args.get("q", "").strip()[:100]
    if search:
        clauses.append("p.nombre LIKE %s")
        values.append(f"%{search}%")
    category = request.args.get("categoria_id")
    if category:
        if not category.isdecimal() or not 1 <= int(category) <= 2147483647:
            raise ValueError("categoria_id: debe ser un entero positivo válido.")
        clauses.append("p.categoria_id = %s")
        values.append(int(category))
    if request.args.get("disponibles") == "1":
        clauses.append("p.stock > 0")
    if request.args.get("destacadas") == "1":
        clauses.append("p.destacada = TRUE")
    sql = PLANT_SELECT + (" WHERE " + " AND ".join(clauses) if clauses else "")
    return jsonify(db.query(sql + " ORDER BY p.nombre", tuple(values)))


@api.get("/plantas/<int:plant_id>")
def get_plant(plant_id):
    plant = db.query(PLANT_SELECT + " WHERE p.id = %s", (plant_id,), one=True)
    if plant is None:
        abort(404)
    return jsonify(plant)


@api.post("/plantas")
def create_plant():
    data = validate_plant(body())
    fields = ", ".join(PLANT_FIELDS)
    placeholders = ", ".join(["%s"] * len(PLANT_FIELDS))
    plant_id = db.execute(f"INSERT INTO plantas ({fields}) VALUES ({placeholders})",
                          tuple(data[field] for field in PLANT_FIELDS))
    return get_plant(plant_id), 201


@api.put("/plantas/<int:plant_id>")
def update_plant(plant_id):
    get_plant(plant_id)
    data = validate_plant(body())
    assignments = ", ".join(f"{field} = %s" for field in PLANT_FIELDS)
    db.execute(f"UPDATE plantas SET {assignments} WHERE id = %s",
               tuple(data[field] for field in PLANT_FIELDS) + (plant_id,))
    return get_plant(plant_id)


@api.delete("/plantas/<int:plant_id>")
def delete_plant(plant_id):
    get_plant(plant_id)
    db.execute("DELETE FROM plantas WHERE id = %s", (plant_id,))
    return "", 204


@api.get("/categorias")
def list_categories():
    return jsonify(db.query("SELECT id, nombre, descripcion FROM categorias ORDER BY nombre"))


@api.get("/categorias/<int:category_id>")
def get_category(category_id):
    category = db.query("SELECT * FROM categorias WHERE id = %s", (category_id,), one=True)
    if category is None:
        abort(404)
    return jsonify(category)


def category_data():
    data = body()
    return text(data, "nombre", 80, True), text(data, "descripcion", 255)


@api.post("/categorias")
def create_category():
    category_id = db.execute("INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s)", category_data())
    return get_category(category_id), 201


@api.put("/categorias/<int:category_id>")
def update_category(category_id):
    get_category(category_id)
    db.execute("UPDATE categorias SET nombre = %s, descripcion = %s WHERE id = %s",
               category_data() + (category_id,))
    return get_category(category_id)


@api.delete("/categorias/<int:category_id>")
def delete_category(category_id):
    get_category(category_id)
    db.execute("DELETE FROM categorias WHERE id = %s", (category_id,))
    return "", 204
