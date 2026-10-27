"""DELETE con ORM. La base elimina también sus pedidos por ON DELETE CASCADE."""
import argparse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from conexion_sqlalchemy import Cliente, crear_motor


def eliminar_cliente(session, cliente_id):
    cliente = session.get(Cliente, cliente_id)
    if cliente is None:
        return False
    session.delete(cliente)
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cliente_id", type=int)
    args = parser.parse_args()
    if args.cliente_id <= 0:
        parser.error("El ID debe ser positivo.")
    motor = crear_motor()
    try:
        with Session(motor) as session:
            with session.begin():
                eliminado = eliminar_cliente(session, args.cliente_id)
        print("Cliente eliminado." if eliminado else "No existe ese cliente.")
    except SQLAlchemyError as error:
        print(f"Error al eliminar: {error}")
        raise SystemExit(1)
    finally:
        motor.dispose()


if __name__ == "__main__":
    main()
