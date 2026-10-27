"""Validación y acceso a los métodos CRUD existentes, sin código de interfaz."""
from pathlib import Path
import sys

import mysql.connector

DB_DIR = Path(__file__).resolve().parents[1] / "db"
if str(DB_DIR) not in sys.path:
    sys.path.insert(0, str(DB_DIR))

from consultar_cliente import consultar_clientes
from insertar_cliente import insertar_cliente
from actualizar_cliente import actualizar_cliente_completo
from eliminar_cliente import eliminar_cliente

CAMPOS = ("Nombre", "Apellido1", "Apellido2", "Ciudad", "Categoria")


def validar_cliente(valores):
    """Respeta longitudes, campos obligatorios, NULL y categoría UNSIGNED."""
    datos = {}
    for campo, maximo in (("Nombre", 25), ("Apellido1", 25), ("Apellido2", 25), ("Ciudad", 35)):
        texto = str(valores.get(campo) or "").strip()
        if campo in ("Nombre", "Apellido1") and not texto:
            raise ValueError(f"El campo {campo} es obligatorio.")
        if len(texto) > maximo:
            raise ValueError(f"{campo} admite como máximo {maximo} caracteres.")
        datos[campo] = texto or None
    categoria = str(valores.get("Categoria") if valores.get("Categoria") is not None else "").strip()
    if categoria:
        if not categoria.isascii() or not categoria.isdecimal():
            raise ValueError("La categoría debe ser un entero no negativo o quedar vacía.")
        numero = int(categoria)
        if numero > 4294967295:
            raise ValueError("La categoría no puede superar 4294967295.")
        datos["Categoria"] = numero
    else:
        datos["Categoria"] = None
    return datos


def filtro_busqueda(texto):
    texto = texto.strip()
    if texto.isascii() and texto.isdecimal():
        return {"cliente_id": int(texto)}
    return {"nombre": texto or None}


class ClientesMySQL:
    def __init__(self, configuracion):
        # La contraseña se conserva solo en memoria; cada trabajo abre su conexión.
        self.configuracion = dict(configuracion)

    def _conexion(self):
        return mysql.connector.connect(
            **self.configuracion, charset="utf8mb4", connection_timeout=8,
            read_timeout=15, write_timeout=15,
        )

    def listar(self, busqueda=""):
        conexion = self._conexion()
        try:
            return consultar_clientes(conexion, **filtro_busqueda(busqueda))
        finally:
            conexion.close()

    def guardar(self, cliente_id, valores):
        datos = validar_cliente(valores)
        conexion = self._conexion()
        try:
            argumentos = [datos[campo] for campo in CAMPOS]
            if cliente_id is None:
                cliente_id = insertar_cliente(conexion, *argumentos)
            elif not actualizar_cliente_completo(conexion, cliente_id, *argumentos):
                raise ValueError("El cliente ya no existe. Actualiza la lista.")
            conexion.commit()
            return cliente_id
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    def eliminar(self, cliente_id):
        conexion = self._conexion()
        try:
            if not eliminar_cliente(conexion, cliente_id):
                raise ValueError("El cliente ya no existe. Actualiza la lista.")
            conexion.commit()
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()


class ClientesDemo:
    """Permite explorar la interfaz sin servidor. Los cambios no se guardan."""
    def __init__(self):
        self.filas = {
            1: dict(idCliente=1, Nombre="Lucía", Apellido1="Gómez", Apellido2="Martínez", Ciudad="Valencia", Categoria=150),
            2: dict(idCliente=2, Nombre="José Luis", Apellido1="Rivero", Apellido2=None, Ciudad="Sevilla", Categoria=200),
            3: dict(idCliente=3, Nombre="Ana", Apellido1="López", Apellido2="Ruiz", Ciudad="Madrid", Categoria=None),
        }
        self.siguiente_id = 4

    def listar(self, busqueda=""):
        filtro = filtro_busqueda(busqueda)
        filas = sorted(self.filas.values(), key=lambda fila: fila["idCliente"])
        if "cliente_id" in filtro:
            filas = [f for f in filas if f["idCliente"] == filtro["cliente_id"]]
        elif filtro.get("nombre"):
            texto = filtro["nombre"].casefold()
            filas = [f for f in filas if texto in " ".join(str(f.get(c) or "") for c in CAMPOS[:3]).casefold()]
        return [dict(f) for f in filas]

    def guardar(self, cliente_id, valores):
        datos = validar_cliente(valores)
        if cliente_id is None:
            cliente_id = self.siguiente_id
            self.siguiente_id += 1
        elif cliente_id not in self.filas:
            raise ValueError("El cliente ya no existe.")
        self.filas[cliente_id] = dict(idCliente=cliente_id, **datos)
        return cliente_id

    def eliminar(self, cliente_id):
        if cliente_id not in self.filas:
            raise ValueError("El cliente ya no existe.")
        del self.filas[cliente_id]
