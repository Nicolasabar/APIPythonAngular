from . import categoria
from ..database.db_mysql import get_connecction


def delete_category(id):
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
