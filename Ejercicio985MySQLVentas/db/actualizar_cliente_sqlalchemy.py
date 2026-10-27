"""UPDATE con ORM: recuperar el objeto y modificar sus atributos."""
import argparse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from conexion_sqlalchemy import Cliente, crear_motor


def actualizar_cliente(session, cliente_id, ciudad, categoria):
    cliente = session.get(Cliente, cliente_id, with_for_update=True)
    if cliente is None:
        return False
    cliente.Ciudad = ciudad
    cliente.Categoria = categoria
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cliente_id", type=int)
    parser.add_argument("ciudad")
    parser.add_argument("categoria", type=int)
    args = parser.parse_args()
    if args.cliente_id <= 0 or args.categoria < 0:
        parser.error("El ID debe ser positivo y la categoría no negativa.")
    motor = crear_motor()
    try:
        with Session(motor) as session:
            # Confirma los cambios al salir; revierte si hay una excepción.
            with session.begin():
                encontrado = actualizar_cliente(session, args.cliente_id, args.ciudad, args.categoria)
        print("Cliente actualizado." if encontrado else "No existe ese cliente.")
    except SQLAlchemyError as error:
        print(f"Error al actualizar: {error}")
        raise SystemExit(1)
    finally:
        motor.dispose()


if __name__ == "__main__":
    main()
