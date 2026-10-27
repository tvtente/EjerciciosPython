"""Motor compartido; reutiliza el modelo Cliente del ejemplo de inserción."""
from sqlalchemy import URL, create_engine
from conexion_mysql import configuracion
from insertar_cliente_sqlalchemy import Cliente


def crear_motor():
    datos = configuracion()
    url = URL.create(
        "mysql+mysqlconnector", username=datos["user"],
        password=datos["password"], host=datos["host"], port=datos["port"],
        database=datos["database"], query={"charset": "utf8mb4"},
    )
    return create_engine(url, hide_parameters=True)
