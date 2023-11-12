from flask import Blueprint, jsonify
from ..models import categoria, categoria_delete, categoria_add, categoria_update
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


@main.route('/update', methods=['PUT'])
def index_update():

    try:

        data = request.get_json()

        if 'id' not in data or 'nombre' not in data or 'precio' not in data:
            raise ValueError("Los datos de entrada no son validos.")
        
        id_update = data['id']
        nombre = data['nombre']
        precio = data['precio']

        result = categoria_update.update_category(id_update, nombre, precio)
        return jsonify({'message': result})
    
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400  # Código de estado 400 para solicitud incorrecta

    except Exception as e:
        return jsonify({'error': f'Error en la actualización: {str(e)}'}), 500  # Código de estado 500 para error interno del servidor