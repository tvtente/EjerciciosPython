"""Conexión compartida por los ejemplos con mysql.connector."""
import os
from getpass import getpass
import mysql.connector


def configuracion():
    password = os.environ.get("MYSQL_PASSWORD")
    if password is None:
        password = getpass("Contraseña de MySQL: ")
    return dict(
        host=os.environ.get("MYSQL_HOST", "127.0.0.1"),
        port=int(os.environ.get("MYSQL_PORT", "3306")),
        user=os.environ.get("MYSQL_USER", "root"),
        password=password,
        database=os.environ.get("MYSQL_DATABASE", "ventas"),
        charset="utf8mb4",
    )


def conectar():
    return mysql.connector.connect(**configuracion())
