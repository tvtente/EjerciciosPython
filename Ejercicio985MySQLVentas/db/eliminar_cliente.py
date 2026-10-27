"""DELETE: eliminar por ID. En el esquema ventas también borra sus pedidos por CASCADE."""
import argparse
from mysql.connector import Error
from conexion_mysql import conectar


def eliminar_cliente(conexion, cliente_id):
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM cliente WHERE idCliente = %s", (cliente_id,))
        return cursor.rowcount > 0
    finally:
        cursor.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cliente_id", type=int)
    args = parser.parse_args()
    if args.cliente_id <= 0:
        parser.error("El ID debe ser positivo.")
    conexion = None
    try:
        conexion = conectar()
        eliminado = eliminar_cliente(conexion, args.cliente_id)
        conexion.commit()
        print("Cliente eliminado." if eliminado else "No existe ese cliente.")
    except Error as error:
        if conexion is not None:
            conexion.rollback()
        print(f"Error al eliminar: {error}")
        raise SystemExit(1)
    finally:
        if conexion is not None:
            conexion.close()


if __name__ == "__main__":
    main()
