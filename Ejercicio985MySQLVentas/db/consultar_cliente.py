"""READ: consultar clientes mediante SELECT y parámetros seguros."""
import argparse
from mysql.connector import Error
from conexion_mysql import conectar


def consultar_clientes(conexion, cliente_id=None, nombre=None):
    sql = "SELECT idCliente, Nombre, Apellido1, Apellido2, Ciudad, Categoria FROM cliente WHERE 1=1"
    parametros = []
    if cliente_id is not None:
        sql += " AND idCliente = %s"
        parametros.append(cliente_id)
    if nombre is not None:
        sql += " AND CONCAT_WS(' ', Nombre, Apellido1, Apellido2) LIKE %s"
        parametros.append(f"%{nombre}%")
    sql += " ORDER BY idCliente"
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute(sql, tuple(parametros))
        return cursor.fetchall()
    finally:
        cursor.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", type=int, dest="cliente_id")
    parser.add_argument("--nombre", help="Parte del nombre o apellidos")
    args = parser.parse_args()
    conexion = None
    try:
        conexion = conectar()
        clientes = consultar_clientes(conexion, args.cliente_id, args.nombre)
        for cliente in clientes:
            print(cliente)
        if not clientes:
            print("No se encontraron clientes.")
    except Error as error:
        print(f"Error al consultar: {error}")
        raise SystemExit(1)
    finally:
        if conexion is not None:
            conexion.close()


if __name__ == "__main__":
    main()
