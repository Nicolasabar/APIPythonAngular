from . import categoria
from ..database.db_mysql import get_connecction


def add_category(nombre, precio, padre_id):
    connection = get_connecction()  # Asumiendo que esta función obtiene una conexión válida

    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO categorias (nombre, precio, padre_id) VALUES (%s, %s, %s)"
            cursor.execute(query, (nombre, precio, padre_id))
            connection.commit()
        return 'Agregado con éxito'
    except Exception as e:
        return f'No se pudo agregar, error: {e}'
    finally:
        connection.close()
