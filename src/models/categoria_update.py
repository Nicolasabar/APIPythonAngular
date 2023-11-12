from . import categoria
from ..database.db_mysql import get_connecction


def update_category(id, nombre, precio):
    connection = get_connecction()
    try:
        with connection.cursor() as cursor:
            query = """
                UPDATE categorias
                SET nombre = %s, 
                    precio = %s
                WHERE id = %s;
            """
            cursor.execute(query, (nombre, precio, id))  # Corregido: se deben pasar nombre, precio e id
            connection.commit()
        return 'Actualizado con éxito'
    except Exception as e:
        return f'No se pudo actualizar, error: {e}'
    finally:
        connection.close()
