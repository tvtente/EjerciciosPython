"""La misma app de clientes con el diseño cargado desde clientes.ui.

Los métodos CRUD, hilos, validación y confirmaciones se heredan de ClientesApp.
Pygubu conecta los comandos y bindings del XML con estos métodos reales.
"""
import argparse
from pathlib import Path

import pygubu
import ttkbootstrap as ttk

from app import ClientesApp
from clientes_datos import CAMPOS


class ClientesPygubuApp(ClientesApp):
    def _interfaz(self):
        self.builder = pygubu.Builder()
        self.builder.add_from_file(Path(__file__).with_name("clientes.ui"))
        self.principal = self.builder.get_object("principal", self)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Asociar las StringVar del XML con el controlador ya existente.
        for nombre in ("busqueda", "estado", "cantidad", "id_texto"):
            anterior = getattr(self, nombre)
            variable = self.builder.get_variable(nombre)
            variable.set(anterior.get())
            setattr(self, nombre, variable)
        for clave, anterior in list(self.config.items()):
            variable = self.builder.get_variable("config_" + clave)
            variable.set(anterior.get())
            self.config[clave] = variable
        for campo, anterior in list(self.campos.items()):
            variable = self.builder.get_variable("campo_" + campo)
            variable.set(anterior.get())
            self.campos[campo] = variable

        # Los ID del diseñador se corresponden con los atributos que usa la app.
        for nombre in (
            "entrada_busqueda", "tabla", "conectar_btn", "buscar_btn", "todos_btn",
            "guardar_btn", "nuevo_btn", "eliminar_btn", "scroll_vertical", "scroll_horizontal",
        ):
            setattr(self, nombre, self.builder.get_object(nombre))
        self.controles = [self.builder.get_object("entrada_" + clave) for clave in self.config]
        self.controles += [self.builder.get_object("campo_" + campo) for campo in CAMPOS]
        self.controles += [
            self.entrada_busqueda, self.conectar_btn, self.buscar_btn, self.todos_btn,
            self.guardar_btn, self.nuevo_btn, self.eliminar_btn,
        ]

        # Los widgets ttk estándar del .ui reciben el estilo de ttkbootstrap.
        for nombre, estilo in {
            "conectar_btn": "primary", "buscar_btn": "primary outline",
            "todos_btn": "secondary outline", "guardar_btn": "success",
            "nuevo_btn": "secondary outline", "eliminar_btn": "danger outline",
            "tabla": "primary", "cliente_id": "primary", "aviso_demo": "warning",
        }.items():
            ttk.apply_bootstyle(self.builder.get_object(nombre), estilo)
        for nombre in ("marca", "introduccion", "ayuda_busqueda", "ayuda_formulario", "contador", "etiqueta_estado"):
            ttk.apply_bootstyle(self.builder.get_object(nombre), "secondary")

        if self.demo:
            self.builder.get_object("aviso_demo").configure(text="DEMO: conexión desactivada")

        # Conecta botones, selección del Treeview, Enter y barras de desplazamiento.
        # Si falta un método, fallar al arrancar en lugar de dejar botones inactivos.
        faltantes = self.builder.connect_callbacks(self)
        if faltantes:
            raise RuntimeError("Callbacks sin implementar: " + ", ".join(faltantes))

    def on_buscar_enter(self, _evento=None):
        self.buscar()
        return "break"

    def on_conectar_enter(self, _evento=None):
        self.conectar()
        return "break"

    def on_guardar_enter(self, _evento=None):
        self.guardar()
        return "break"

    def on_editar_doble_click(self, _evento=None):
        if not self.ocupado:
            self._seleccionar()
            self.builder.get_object("campo_Nombre").focus_set()

    def on_scroll_vertical(self, *argumentos):
        self.tabla.yview(*argumentos)

    def on_scroll_horizontal(self, *argumentos):
        self.tabla.xview(*argumentos)

    def on_tabla_yview(self, primero, ultimo):
        self.scroll_vertical.set(primero, ultimo)

    def on_tabla_xview(self, primero, ultimo):
        self.scroll_horizontal.set(primero, ultimo)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true", help="Probar sin MySQL")
    args = parser.parse_args()
    ClientesPygubuApp(demo=args.demo).mainloop()


if __name__ == "__main__":
    main()
