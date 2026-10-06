"""Lógica compartida: Pygubu carga el diseño; Python conecta sus acciones.

Ambas variantes reutilizan control_eventos.py y su archivo asistentes.json.
Edita el aspecto en eventos_pack.ui o eventos_grid.ui con Pygubu Designer.
"""
from pathlib import Path
from tkinter import StringVar, messagebox
import pygubu
import ttkbootstrap as ttk
from control_eventos import ARCHIVO, CAMPOS, ControlEventos, cargar_datos


class EventosPygubu(ControlEventos):
    def __init__(self, ventana, datos, gestor):
        # Reutilizamos registrar_asistente, actualizar_tabla, ver_json y exportar de la
        # aplicación anterior; aquí construimos la interfaz desde el archivo UI.
        self.ventana = ventana
        self.datos = datos
        self.builder = pygubu.Builder()
        archivo_ui = Path(__file__).with_name(f"eventos_{gestor}.ui")
        self.builder.add_from_file(str(archivo_ui))
        self.principal = self.builder.get_object("principal", ventana)
        if gestor == "grid":
            # weight=1 permite que la fila/columna crezca con la ventana.
            ventana.rowconfigure(0, weight=1)
            ventana.columnconfigure(0, weight=1)

        self.campos = {c: StringVar(master=ventana) for c in CAMPOS[1:5]}
        for campo, variable in self.campos.items():
            self.builder.get_object(f"entrada_{campo}").configure(textvariable=variable)
        self.campos["categoria"].set("General")
        self.entrada_nombre = self.builder.get_object("entrada_nombre")
        self.busqueda = StringVar(master=ventana)
        self.builder.get_object("entrada_buscar").configure(textvariable=self.busqueda)
        self.estado = StringVar(master=ventana, value=f"Ejemplo {gestor} · Guardado automático: {ARCHIVO.name}")
        self.builder.get_object("estado").configure(textvariable=self.estado)
        self.total = self.builder.get_object("total")
        self.tabla = self.builder.get_object("tabla")
        scroll = self.builder.get_object("scroll")
        scroll.configure(command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        # command recibe la función sin paréntesis: se ejecuta al pulsar.
        self.builder.get_object("registrar").configure(command=self.registrar_asistente)
        self.builder.get_object("ver_json").configure(command=self.ver_json)
        self.builder.get_object("exportar").configure(command=self.exportar)
        self.busqueda.trace_add("write", lambda *_: self.actualizar_tabla())
        self.actualizar_tabla()
        self.entrada_nombre.focus_set()


def iniciar(gestor):
    ventana = ttk.Window(title=f"Control de eventos — {gestor}", themename="flatly")
    ventana.geometry("900x620")
    ventana.minsize(820, 560)
    try:
        datos = cargar_datos(ARCHIVO)
    except (OSError, ValueError) as error:
        messagebox.showerror("No se pudo cargar el JSON", str(error), parent=ventana)
        ventana.destroy()
        return
    EventosPygubu(ventana, datos, gestor)
    ventana.mainloop()
