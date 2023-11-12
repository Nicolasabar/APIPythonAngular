from . import categoria
from ..database.db_mysql import get_connecction


def validate_children(id):
    connection = get_connecction()
    try:
        with connection.cursor() as cursor:
            query = "SELECT COUNT(*) FROM categorias WHERE padre_id = %s"
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            return result[0] > 0
    except Exception as e:
        print(f'Error al verificar si tiene hijos: {e}')
        return False
    finally:
        connection.close()


def delete_category(id):
    if validate_children(id):
        return 'No se puede eliminar, el elemento tiene hijos asociados.'
    
    connection = get_connecction()
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM categorias WHERE id = %s"
            cursor.execute(query, (id,))
            connection.commit()
        return 'Eliminado con éxito'
    except Exception as e:
        return f'No se pudo eliminar, error: {e}'
    finally:
        connection.close()

