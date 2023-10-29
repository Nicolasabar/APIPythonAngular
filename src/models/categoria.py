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

def serialize_categoria(categoria):
    if isinstance(categoria, Categoria):
        # Crear una copia de la categoría para no modificar la original
        serialized_categoria = {
            'id': categoria.id,
            'nombre': categoria.nombre,
            'padre_id': categoria.padre_id,
            'subcategorias': [serialize_categoria(subcategoria) for subcategoria in categoria.subcategorias]
        }

        # Convertir el precio a flotante si es un Decimal
        if isinstance(categoria.precio, Decimal):
            serialized_categoria['precio'] = float(categoria.precio)
        else:
            serialized_categoria['precio'] = categoria.precio

        return serialized_categoria

    return categoria