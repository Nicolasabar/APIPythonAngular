from flask import Blueprint, jsonify
from ..models import categoria
from flask_json import FlaskJSON  


main = Blueprint('index_blueprint', __name__)


@main.route('/')
def index():
    data = categoria.getTree()

    # Convierte la estructura jerárquica en una lista de diccionarios
    categorias = [categoria.serialize_categoria(categoria.Categoria(*row)) for row in data]

    # Devuelve la lista de categorías en formato JSON
    return jsonify(categorias)