# Importar las dependencias necesarias
from ..database.db_mysql import get_connecction
from decimal import Decimal
from flask import render_template, jsonify

class Categoria:
    def __init__(self, id, nombre, padre_id, precio):
        self.id = id
        self.nombre = nombre
        self.padre_id = padre_id
        self.precio = precio
        self.subcategorias = []

    def to_dict(self):
        # Convierte un objeto Categoria a un diccionario
        return {
            'id': self.id,
            'nombre': self.nombre,
            'padre_id': self.padre_id,
            'precio': self.precio,
            'subcategorias': [subcategoria.to_dict() for subcategoria in self.subcategorias]
        }

def getTree():
    connection = get_connecction()
    try:
        with connection.cursor() as cursor:
            # Consulta recursiva
            query = """
            WITH RECURSIVE CategoryTree AS (
                SELECT id, nombre, padre_id, precio
                FROM categorias
                WHERE padre_id IS NULL  -- Comienza desde las categorías principales
              
                UNION ALL
              
                SELECT c.id, c.nombre, c.padre_id, c.precio
                FROM categorias c
                INNER JOIN CategoryTree ct ON c.padre_id = ct.id
            )
            SELECT id, nombre, padre_id, precio
            FROM CategoryTree
            ORDER BY id;
            """
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()

def serialize_categoria(categorias):
    # Crear un diccionario para mapear categorías por su ID
    categoria_dict = {categoria['id']: categoria for categoria in categorias}

    # Inicializar una lista de categorías raíz
    root_categorias = []

    # Iterar a través de las categorías para construir la estructura de árbol
    for categoria in categorias:
        if categoria['padre_id'] is None:
            # Esta es una categoría raíz
            root_categorias.append(categoria)
        else:
            # Esta es una subcategoría, agreguémosla a su padre correspondiente
            parent_categoria = categoria_dict.get(categoria['padre_id'])
            if parent_categoria is not None:
                if 'subcategorias' not in parent_categoria:
                    parent_categoria['subcategorias'] = []
                parent_categoria['subcategorias'].append(categoria)

    return root_categorias



def convert_to_tree_data(categorias):
    # Crear un diccionario para mapear categorías por su ID
    categoria_dict = {categoria.id: categoria for categoria in categorias}

    # Inicializar una lista de categorías raíz
    root_categorias = []

    # Iterar a través de las categorías para construir la estructura de árbol
    for categoria in categorias:
        if categoria.padre_id is None:
            # Esta es una categoría raíz
            root_categorias.append(categoria)
        else:
            # Esta es una subcategoría, agreguémosla a su padre correspondiente
            parent_categoria = categoria_dict.get(categoria.padre_id)
            if parent_categoria is not None:
                if not hasattr(parent_categoria, 'subcategorias'):
                    parent_categoria.subcategorias = []
                parent_categoria.subcategorias.append(categoria)

    # Convertir la estructura en el formato deseado
    def to_tree_format(categoria):
        tree_categoria = {'name': categoria.nombre}
        if categoria.precio is not None:
            tree_categoria['price'] = float(categoria.precio)
        if hasattr(categoria, 'subcategorias'):
            tree_categoria['children'] = [to_tree_format(subcategoria) for subcategoria in categoria.subcategorias]
        return tree_categoria

    # Obtener la estructura de datos en el formato deseado
    tree_data = [to_tree_format(categoria) for categoria in root_categorias]

    return tree_data
