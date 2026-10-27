"""READ con SQLAlchemy: select(Cliente) devuelve objetos del modelo."""
import argparse
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from conexion_sqlalchemy import Cliente, crear_motor


def consultar_clientes(session, cliente_id=None, nombre=None):
    consulta = select(Cliente).order_by(Cliente.idCliente)
    if cliente_id is not None:
        consulta = consulta.where(Cliente.idCliente == cliente_id)
    if nombre is not None:
        nombre_completo = func.concat_ws(" ", Cliente.Nombre, Cliente.Apellido1, Cliente.Apellido2)
        consulta = consulta.where(nombre_completo.like(f"%{nombre}%"))
    return session.scalars(consulta).all()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", type=int, dest="cliente_id")
    parser.add_argument("--nombre", help="Parte del nombre o apellidos")
    args = parser.parse_args()
    motor = crear_motor()
    try:
        with Session(motor) as session:
            clientes = consultar_clientes(session, args.cliente_id, args.nombre)
            for c in clientes:
                print(dict(idCliente=c.idCliente, Nombre=c.Nombre, Apellido1=c.Apellido1,
                           Apellido2=c.Apellido2, Ciudad=c.Ciudad, Categoria=c.Categoria))
            if not clientes:
                print("No se encontraron clientes.")
    except SQLAlchemyError as error:
        print(f"Error al consultar: {error}")
        raise SystemExit(1)
    finally:
        motor.dispose()


if __name__ == "__main__":
    main()
