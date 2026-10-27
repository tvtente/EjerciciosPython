"""Inserta el mismo cliente que insertar_cliente.py usando SQLAlchemy ORM.

Dependencias: python -m pip install sqlalchemy mysql-connector-python
La tabla cliente debe existir en la base ventas; este script no crea tablas.
"""

import os
from getpass import getpass

from sqlalchemy import String, URL, create_engine
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class Cliente(Base):
    """Representa la tabla cliente y sus columnas existentes."""

    __tablename__ = "cliente"

    idCliente: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), primary_key=True, autoincrement=True
    )
    Nombre: Mapped[str] = mapped_column(String(25))
    Apellido1: Mapped[str] = mapped_column(String(25))
    Apellido2: Mapped[str | None] = mapped_column(String(25))
    Ciudad: Mapped[str | None] = mapped_column(String(35))
    Categoria: Mapped[int | None] = mapped_column(INTEGER(unsigned=True))


def main() -> None:
    # 1. Configurar la misma conexión local a ventas.
    # Si MYSQL_PASSWORD no está definida, solicita la contraseña sin mostrarla.
    password = os.environ.get("MYSQL_PASSWORD")
    if password is None:
        password = getpass("Contraseña de MySQL: ")

    url = URL.create(
        drivername="mysql+mysqlconnector",
        username=os.environ.get("MYSQL_USER", "root"),
        password=password,
        host=os.environ.get("MYSQL_HOST", "127.0.0.1"),
        port=int(os.environ.get("MYSQL_PORT", "3306")),
        database=os.environ.get("MYSQL_DATABASE", "ventas"),
        query={"charset": "utf8mb4"},
    )
    # URL.create admite contraseñas con caracteres especiales como @ o :.
    engine = create_engine(url, hide_parameters=True)

    try:
        # 2. Crear un objeto en lugar de escribir INSERT INTO ... VALUES.
        nuevo_cliente = Cliente(
            Nombre="Gustavo",
            Apellido1="Moyano",
            Apellido2="Díaz",
            Ciudad="Barcelona",
            Categoria=150,
        )

        # 3. La sesión traduce el objeto a un INSERT con parámetros seguros.
        # begin confirma al terminar; ante un error revierte la transacción.
        # Los bloques with cierran la transacción y la sesión automáticamente.
        with Session(engine) as session:
            with session.begin():
                session.add(nuevo_cliente)
                session.flush()  # Ejecuta el INSERT y obtiene el AUTO_INCREMENT.
                id_asignado = nuevo_cliente.idCliente

        # 4. Mostrar éxito solo después de confirmar el commit.
        print(f"¡Registro insertado correctamente! ID asignado: {id_asignado}")

    except SQLAlchemyError as error:
        print(f"Error al conectar o interactuar con la base de datos: {error}")
    finally:
        # 5. Liberar las conexiones del motor.
        engine.dispose()
        print("Conexiones del motor cerradas.")


if __name__ == "__main__":
    main()
