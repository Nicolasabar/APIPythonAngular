from flask import Blueprint, jsonify
from ..models import categoria
from flask_cors import CORS


main = Blueprint('index_blueprint', __name__)
CORS(main)

@main.route('/')
def index():
    data = categoria.getTree()

    categorias = [categoria.Categoria(row[0], row[1], row[2], row[3]) for row in data]

    # Convertir la estructura de categorías a la deseada
    tree_data = categoria.convert_to_tree_data(categorias)

    # Devuelve la estructura de datos en formato JSON
    return jsonify(tree_data)