from . import categoria
from ..database.db_mysql import get_connecction
from .categoria_add import validate_name, validate_price


def update_category(id, nombre, precio):
    connection = get_connecction()

    # validar largo de nombre al actualizar
    result = validate_name(nombre)
    v_price = validate_price(precio)
    
    if result is True and v_price is True:
        
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
