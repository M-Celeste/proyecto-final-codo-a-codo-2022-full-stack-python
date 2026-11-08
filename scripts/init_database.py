"""Inicializa una base ya creada por el proveedor, sin CREATE DATABASE ni USE.

Ejecutar desde la raíz: python -m scripts.init_database
Lee la conexión del entorno o .env. No muestra credenciales.
El separador sirve para los SQL de este repositorio (sin rutinas ni delimitadores
personalizados). No utilizar como importador genérico de archivos SQL.
"""
import re
from pathlib import Path

from mysql.connector import Error
from raiz_celeste import create_app
from raiz_celeste.db import get_db


def statements(source):
    source = re.sub(r"^\s*--[^\n]*", "", source, flags=re.MULTILINE)
    for statement in source.split(";"):
        statement = statement.strip()
        if statement and not re.match(r"^(CREATE\s+DATABASE|USE)\b", statement, re.IGNORECASE):
            yield statement


def main():
    root = Path(__file__).resolve().parent.parent
    app = create_app()
    with app.app_context():
        connection = get_db()
        cursor = connection.cursor()
        try:
            for name in ("01_schema.sql", "02_seed.sql", "03_fotografias.sql"):
                for statement in statements((root / "database" / name).read_text(encoding="utf-8")):
                    cursor.execute(statement)
            connection.commit()
            print("Esquema y datos de demostración importados.")
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()


if __name__ == "__main__":
    try:
        main()
    except Error as error:
        raise SystemExit(f"No se pudo inicializar la base (código {error.errno}). Revisá la conexión y los permisos.") from None
