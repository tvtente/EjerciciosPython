#!/usr/bin/python3
"""
titulo del pack

descripción de pack

UI source file: eventos_pack.ui
"""
import tkinter as tk
import tkinter.ttk as ttk


def safe_i18n_translator(value):
    """i18n - Setup translator in derived class file"""
    return value


def safe_fo_callback(widget):
    """on first objec callback - Setup callback in derived class file."""
    pass


def safe_image_loader(master, image_name: str):
    """Image loader - Setup image_loader in derived class file."""
    img = None
    try:
        img = tk.PhotoImage(file=image_name, master=master)
    except tk.TclError:
        pass
    return img


class ControlEventosPackUI:
    def __init__(
        self,
        master=None,
        *,
        translator=None,
        on_first_object_cb=None,
        data_pool=None,
        image_loader=None
    ):
        if translator is None:
            translator = safe_i18n_translator
        _ = translator  # i18n string marker.
        if image_loader is None:
            image_loader = safe_image_loader
        if on_first_object_cb is None:
            on_first_object_cb = safe_fo_callback
        # build ui
        self.principal = ttk.Frame(master, name="principal")
        self.principal.configure(padding=18)
        # First object created
        on_first_object_cb(self.principal)

        self.titulo = ttk.Label(self.principal, name="titulo")
        self.titulo.configure(
            anchor="center",
            font="{Sans} 20 bold",
            text='Control de Entrada a Evento')
        self.titulo.pack(fill="x", pady="5 20")
        self.formulario = ttk.Labelframe(self.principal, name="formulario")
        self.formulario.configure(padding=15, text='Registrar Nuevo Asistente')
        self.fila_0 = ttk.Frame(self.formulario, name="fila_0")
        self.grupo_nombre = ttk.Frame(self.fila_0, name="grupo_nombre")
        self.etiqueta_nombre = ttk.Label(
            self.grupo_nombre, name="etiqueta_nombre")
        self.etiqueta_nombre.configure(text='Nombre:', width=10)
        self.etiqueta_nombre.pack(side="left")
        self.entrada_nombre = ttk.Entry(
            self.grupo_nombre, name="entrada_nombre")
        self.entrada_nombre.configure(width=24)
        self.entrada_nombre.pack(expand=True, fill="x", side="left")
        self.grupo_nombre.pack(expand=True, fill="x", padx=5, side="left")
        self.grupo_apellidos = ttk.Frame(self.fila_0, name="grupo_apellidos")
        self.etiqueta_apellidos = ttk.Label(
            self.grupo_apellidos, name="etiqueta_apellidos")
        self.etiqueta_apellidos.configure(text='Apellidos:', width=10)
        self.etiqueta_apellidos.pack(side="left")
        self.entrada_apellidos = ttk.Entry(
            self.grupo_apellidos, name="entrada_apellidos")
        self.entrada_apellidos.configure(width=24)
        self.entrada_apellidos.pack(expand=True, fill="x", side="left")
        self.grupo_apellidos.pack(expand=True, fill="x", padx=5, side="left")
        self.fila_0.pack(fill="x", pady=5)
        self.fila_1 = ttk.Frame(self.formulario, name="fila_1")
        self.grupo_correo = ttk.Frame(self.fila_1, name="grupo_correo")
        self.etiqueta_correo = ttk.Label(
            self.grupo_correo, name="etiqueta_correo")
        self.etiqueta_correo.configure(text='Correo:', width=10)
        self.etiqueta_correo.pack(side="left")
        self.entrada_correo = ttk.Entry(
            self.grupo_correo, name="entrada_correo")
        self.entrada_correo.configure(width=24)
        self.entrada_correo.pack(expand=True, fill="x", side="left")
        self.grupo_correo.pack(expand=True, fill="x", padx=5, side="left")
        self.grupo_categoria = ttk.Frame(self.fila_1, name="grupo_categoria")
        self.etiqueta_categoria = ttk.Label(
            self.grupo_categoria, name="etiqueta_categoria")
        self.etiqueta_categoria.configure(text='Categoría:', width=10)
        self.etiqueta_categoria.pack(side="left")
        self.entrada_categoria = ttk.Combobox(
            self.grupo_categoria, name="entrada_categoria")
        self.entrada_categoria.configure(
            state="readonly",
            values='General VIP Ponente Organización',
            width=24)
        self.entrada_categoria.pack(expand=True, fill="x", side="left")
        self.grupo_categoria.pack(expand=True, fill="x", padx=5, side="left")
        self.fila_1.pack(fill="x", pady=5)
        self.registrar = ttk.Button(self.formulario, name="registrar")
        self.registrar.configure(
            style="success.TButton",
            text='Registrar Entrada')
        self.registrar.pack(fill="x", padx=5, pady="12 5")
        self.formulario.pack(fill="x")
        self.filtros = ttk.Frame(self.principal, name="filtros")
        self.etiqueta_buscar = ttk.Label(self.filtros, name="etiqueta_buscar")
        self.etiqueta_buscar.configure(text='Buscar:')
        self.etiqueta_buscar.pack(side="left")
        self.entrada_buscar = ttk.Entry(self.filtros, name="entrada_buscar")
        self.entrada_buscar.configure(width=28)
        self.entrada_buscar.pack(padx=8, side="left")
        self.total = ttk.Label(self.filtros, name="total")
        self.total.configure(text='Total asistentes: 0')
        self.total.pack(side="right")
        self.filtros.pack(fill="x", pady=15)
        self.tabla_marco = ttk.Frame(self.principal, name="tabla_marco")
        self.scroll = ttk.Scrollbar(self.tabla_marco, name="scroll")
        self.scroll.configure(orient="vertical")
        self.scroll.pack(fill="y", side="right")
        self.tabla = ttk.Treeview(self.tabla_marco, name="tabla")
        self.tabla.configure(height=10, show="headings")
        self.tabla_cols = [
            'id',
            'nombre',
            'apellidos',
            'correo',
            'categoria',
            'hora_entrada']
        self.tabla_dcols = [
            'id',
            'nombre',
            'apellidos',
            'correo',
            'categoria',
            'hora_entrada']
        self.tabla.configure(
            columns=self.tabla_cols,
            displaycolumns=self.tabla_dcols)
        self.tabla.column(
            "id",
            anchor="w",
            stretch=True,
            width=45,
            minwidth=40)
        self.tabla.column(
            "nombre",
            anchor="w",
            stretch=True,
            width=110,
            minwidth=40)
        self.tabla.column(
            "apellidos",
            anchor="w",
            stretch=True,
            width=130,
            minwidth=40)
        self.tabla.column(
            "correo",
            anchor="w",
            stretch=True,
            width=190,
            minwidth=40)
        self.tabla.column(
            "categoria",
            anchor="w",
            stretch=True,
            width=105,
            minwidth=40)
        self.tabla.column(
            "hora_entrada",
            anchor="w",
            stretch=True,
            width=165,
            minwidth=40)
        self.tabla.heading("id", anchor="w", text='ID')
        self.tabla.heading("nombre", anchor="w", text='Nombre')
        self.tabla.heading("apellidos", anchor="w", text='Apellidos')
        self.tabla.heading("correo", anchor="w", text='Correo')
        self.tabla.heading("categoria", anchor="w", text='Categoría')
        self.tabla.heading("hora_entrada", anchor="w", text='Hora de entrada')
        self.tabla.pack(expand=True, fill="both")
        self.tabla_marco.pack(expand=True, fill="both")
        self.acciones = ttk.Frame(self.principal, name="acciones")
        self.ver_json = ttk.Button(self.acciones, name="ver_json")
        self.ver_json.configure(text='Ver JSON')
        self.ver_json.pack(side="left")
        self.exportar = ttk.Button(self.acciones, name="exportar")
        self.exportar.configure(style="success.TButton", text='Exportar JSON…')
        self.exportar.pack(padx=10, side="left")
        self.acciones.pack(fill="x", pady="15 8")
        self.estado = ttk.Label(self.principal, name="estado")
        self.estado.configure(
            text='Guardado automático en asistentes.json',
            wraplength=780)
        self.estado.pack(anchor="w")
        self.principal.pack(expand=True, fill="both")

        # Main widget
        self.mainwindow = self.principal

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = ControlEventosPackUI(root)
    app.run()
