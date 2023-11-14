from . import categoria
from ..database.db_mysql import get_connecction
from pymysql import IntegrityError 


def add_category(nombre, precio, padre_id):
    connection = get_connecction()  # Asumiendo que esta función obtiene una conexión válida
    result = validate_name(nombre)
    v_price = validate_price(precio)

    if result is True and v_price is True:
        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO categorias (nombre, precio, padre_id) VALUES (%s, %s, %s)"
                cursor.execute(query, (nombre, precio, padre_id))
                connection.commit()
                return 'Agregado con éxito'
        except IntegrityError:
            return 'Violación de integridad: el nombre ya existe'
        except Exception as e:
            return f'No se pudo agregar, error: {e}'
        finally:
            connection.close()
    else:
        return f'No se pudo agregar' 


def validate_name(nombre):
    if len(nombre) <= 10:
        return True
    else:
        return 'El largo del nombre es incorrecto. Máximo 10 caracteres.'
    

def validate_price(price):
    if isinstance(price, int) and len(str(price)) <= 10 and price > 0:
        return True
    else:
        raise ValueError('Ingresar valor numérico de longitud máxima 10 y mayor a 0')
    