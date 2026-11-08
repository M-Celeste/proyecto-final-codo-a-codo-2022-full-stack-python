import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, abort, jsonify, render_template, request
from mysql.connector import Error, IntegrityError

from . import db


def create_app(test_config=None):
    root = Path(__file__).resolve().parent.parent
    load_dotenv(root / ".env")
    app = Flask(__name__, template_folder=str(root / "templates"),
                static_folder=str(root / "static"))
    app.config.from_mapping(
        MYSQL_HOST=os.getenv("MYSQL_HOST", "127.0.0.1"),
        MYSQL_PORT=int(os.getenv("MYSQL_PORT", "3306")),
        MYSQL_USER=os.getenv("MYSQL_USER", "root"),
        MYSQL_PASSWORD=os.getenv("MYSQL_PASSWORD", ""),
        MYSQL_DATABASE=os.getenv("MYSQL_DATABASE", "raiz_celeste"),
        MYSQL_SSL=os.getenv("MYSQL_SSL", "false").lower() == "true",
        MYSQL_SSL_CA=os.getenv("MYSQL_SSL_CA", ""),
        PUBLIC_DEMO=os.getenv("VERCEL") == "1" or os.getenv("PUBLIC_DEMO", "false").lower() == "true",
        MAX_CONTENT_LENGTH=64 * 1024,
    )
    if test_config:
        app.config.update(test_config)
    app.json.ensure_ascii = False
    db.init_app(app)

    from .pages import pages
    from .api import api
    app.register_blueprint(pages)
    app.register_blueprint(api, url_prefix="/api")

    @app.before_request
    def protect_public_demo():
        # En Vercel la demostración es de consulta. El CRUD local se conserva.
        if app.config["PUBLIC_DEMO"]:
            if request.path == "/admin" or request.path.startswith("/admin/"):
                abort(404)
            if request.path.startswith("/api/") and request.method not in {"GET", "HEAD", "OPTIONS"}:
                return jsonify(error="La demostración pública es de solo lectura."), 403

    @app.errorhandler(IntegrityError)
    def integrity_error(error):
        db.rollback()
        messages = {
            1062: "Ya existe una categoría con ese nombre.",
            1451: "La categoría tiene plantas. Reasignalas antes de eliminarla.",
            1452: "La categoría seleccionada no existe.",
        }
        return jsonify(error=messages.get(error.errno, "Los datos no cumplen las reglas de la base.")), 409

    @app.errorhandler(Error)
    def database_error(error):
        db.rollback()
        app.logger.error("Error de MySQL: %s", error.errno)
        return jsonify(error="No se pudo acceder a MySQL. Revisá la configuración y la importación de los scripts SQL."), 503

    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith("/api/"):
            return jsonify(error="Recurso no encontrado."), 404
        return render_template("404.html"), 404

    return app
