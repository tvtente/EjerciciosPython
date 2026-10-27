"""CREATE: insertar un cliente con mysql.connector y parámetros seguros."""
import argparse
from mysql.connector import Error
from conexion_mysql import conectar


def insertar_cliente(conexion, nombre, apellido1, apellido2=None, ciudad=None, categoria=None):
    """Inserta el cliente y devuelve su ID; quien llama confirma la transacción."""
    cursor = conexion.cursor()
    try:
        sql = """
            INSERT INTO cliente (Nombre, Apellido1, Apellido2, Ciudad, Categoria)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (nombre, apellido1, apellido2, ciudad, categoria))
        return cursor.lastrowid
    finally:
        cursor.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    # Sin argumentos se conservan los datos del ejemplo original.
    parser.add_argument("--nombre", default="Lucía")
    parser.add_argument("--apellido1", default="Gómez")
    parser.add_argument("--apellido2", default="Martínez")
    parser.add_argument("--ciudad", default="Valencia")
    parser.add_argument("--categoria", type=int, default=150)
    args = parser.parse_args()
    if not args.nombre.strip() or not args.apellido1.strip():
        parser.error("El nombre y el primer apellido no pueden estar vacíos.")
    if args.categoria < 0:
        parser.error("La categoría no puede ser negativa.")

    conexion = None
    try:
        conexion = conectar()
        id_asignado = insertar_cliente(
            conexion, args.nombre, args.apellido1,
            args.apellido2, args.ciudad, args.categoria,
        )
        conexion.commit()
        print(f"¡Registro insertado correctamente! ID asignado: {id_asignado}")
    except Error as error:
        if conexion is not None:
            conexion.rollback()
        print(f"Error al insertar: {error}")
        raise SystemExit(1)
    finally:
        if conexion is not None:
            conexion.close()


if __name__ == "__main__":
    main()
