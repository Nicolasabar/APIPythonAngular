from flask import Blueprint, jsonify
from ..models import categoria, categoria_delete, categoria_add
from flask_cors import CORS
from flask import request


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


@main.route('/delete/<int:id>', methods=['DELETE'])
def index_delete(id):
    result = categoria_delete.delete_category(id)
    return jsonify({'message': result})


@main.route('/add', methods=['POST'])
def index_add():
    data = request.get_json()
    nombre = data.get('nombre')
    precio = data.get('precio')
    id_padre = data.get('id_padre')
    result = categoria_add.add_category(nombre, precio, id_padre)
    return jsonify({'message': result})
