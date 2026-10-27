"""UPDATE: cambiar la ciudad y categoría de un cliente por su ID."""
import argparse
from mysql.connector import Error
from conexion_mysql import conectar


def actualizar_cliente(conexion, cliente_id, ciudad, categoria):
    # Bloquear el registro durante la transacción permite comprobar su existencia.
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT idCliente FROM cliente WHERE idCliente = %s FOR UPDATE", (cliente_id,))
        if cursor.fetchone() is None:
            return False
        cursor.execute(
            "UPDATE cliente SET Ciudad = %s, Categoria = %s WHERE idCliente = %s",
            (ciudad, categoria, cliente_id),
        )
        return True
    finally:
        cursor.close()


def actualizar_cliente_completo(
    conexion, cliente_id, nombre, apellido1, apellido2=None, ciudad=None, categoria=None
):
    """Actualiza el formulario completo; quien llama confirma la transacción."""
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "SELECT idCliente FROM cliente WHERE idCliente = %s FOR UPDATE",
            (cliente_id,),
        )
        if cursor.fetchone() is None:
            return False
        cursor.execute(
            """UPDATE cliente SET Nombre = %s, Apellido1 = %s, Apellido2 = %s,
                      Ciudad = %s, Categoria = %s WHERE idCliente = %s""",
            (nombre, apellido1, apellido2, ciudad, categoria, cliente_id),
        )
        return True
    finally:
        cursor.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cliente_id", type=int)
    parser.add_argument("ciudad")
    parser.add_argument("categoria", type=int)
    args = parser.parse_args()
    if args.cliente_id <= 0 or args.categoria < 0:
        parser.error("El ID debe ser positivo y la categoría no negativa.")
    conexion = None
    try:
        conexion = conectar()
        encontrado = actualizar_cliente(conexion, args.cliente_id, args.ciudad, args.categoria)
        conexion.commit()
        print("Cliente actualizado." if encontrado else "No existe ese cliente.")
    except Error as error:
        if conexion is not None:
            conexion.rollback()
        print(f"Error al actualizar: {error}")
        raise SystemExit(1)
    finally:
        if conexion is not None:
            conexion.close()


if __name__ == "__main__":
    main()
