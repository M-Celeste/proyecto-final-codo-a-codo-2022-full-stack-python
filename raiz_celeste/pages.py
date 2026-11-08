import json
from pathlib import Path
from flask import Blueprint, render_template

pages = Blueprint("pages", __name__)


@pages.get("/creditos")
def credits():
    source = Path(__file__).resolve().parent.parent / 'docs' / 'fotografias.json'
    return render_template('creditos.html', photos=json.loads(source.read_text(encoding='utf-8')))


@pages.get("/")
def home():
    return render_template("inicio.html")


@pages.get("/catalogo")
def catalog():
    return render_template("catalogo.html")


@pages.get("/plantas/<int:plant_id>")
def detail(plant_id):
    return render_template("planta.html", plant_id=plant_id)


@pages.get("/contacto")
def contact():
    return render_template("contacto.html")


@pages.get("/admin/plantas")
def plants():
    return render_template("admin/plantas.html")


@pages.get("/admin/plantas/nueva")
@pages.get("/admin/plantas/<int:plant_id>/editar")
def plant_form(plant_id=None):
    return render_template("admin/planta_formulario.html", plant_id=plant_id)


@pages.get("/admin/categorias")
def categories():
    return render_template("admin/categorias.html")
