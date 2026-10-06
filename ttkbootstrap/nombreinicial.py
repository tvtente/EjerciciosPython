#!/usr/bin/python3
"""
nombre inicial

nombre inicial

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
    return tk.PhotoImage(file=image_name, master=master)


def find_callback(callbacks_bag, callback_uid):
    cb = None

    if isinstance(callbacks_bag, dict):
        if callback_uid in callbacks_bag:
            cb = callbacks_bag[callback_uid]
    elif hasattr(callbacks_bag, callback_uid):
        cb = getattr(callbacks_bag, callback_uid)
    if cb is None:

        def cb_undef(*args):
            print(f"No function defined for {callback_uid}")

        cb = cb_undef
    return cb


def nombreinicial(
    master=None,
    *,
    translator=None,
    on_first_object_cb=None,
    data_pool=None,
    image_loader=None,
    callbacks_bag=None,
):
    if translator is None:
        translator = safe_i18n_translator
    _ = translator  # i18n string marker.
    if image_loader is None:
        image_loader = safe_image_loader
    if on_first_object_cb is None:
        on_first_object_cb = safe_fo_callback

    #
    # Begin UI code
    principal = ttk.Frame(master, name="principal")
    principal.configure(padding=18)
    # First object created
    on_first_object_cb(principal)

    titulo = ttk.Label(principal, name="titulo")
    titulo.configure(
        anchor="center",
        font="{Sans} 20 bold",
        text='Control de Entrada a Evento')
    titulo.pack(fill="x", pady="5 20")
    formulario = ttk.Labelframe(principal, name="formulario")
    formulario.configure(padding=15, text='Registrar Nuevo Asistente')
    fila_0 = ttk.Frame(formulario, name="fila_0")
    grupo_nombre = ttk.Frame(fila_0, name="grupo_nombre")
    etiqueta_nombre = ttk.Label(grupo_nombre, name="etiqueta_nombre")
    etiqueta_nombre.configure(text='Nombre:', width=10)
    etiqueta_nombre.pack(side="left")
    entrada_nombre = ttk.Entry(grupo_nombre, name="entrada_nombre")
    entrada_nombre.configure(width=24)
    entrada_nombre.pack(expand=True, fill="x", side="left")
    grupo_nombre.pack(expand=True, fill="x", padx=5, side="left")
    grupo_apellidos = ttk.Frame(fila_0, name="grupo_apellidos")
    etiqueta_apellidos = ttk.Label(grupo_apellidos, name="etiqueta_apellidos")
    etiqueta_apellidos.configure(text='Apellidos:', width=10)
    etiqueta_apellidos.pack(side="left")
    entrada_apellidos = ttk.Entry(grupo_apellidos, name="entrada_apellidos")
    entrada_apellidos.configure(width=24)
    entrada_apellidos.pack(expand=True, fill="x", side="left")
    grupo_apellidos.pack(expand=True, fill="x", padx=5, side="left")
    fila_0.pack(fill="x", pady=5)
    fila_1 = ttk.Frame(formulario, name="fila_1")
    grupo_correo = ttk.Frame(fila_1, name="grupo_correo")
    etiqueta_correo = ttk.Label(grupo_correo, name="etiqueta_correo")
    etiqueta_correo.configure(text='Correo:', width=10)
    etiqueta_correo.pack(side="left")
    entrada_correo = ttk.Entry(grupo_correo, name="entrada_correo")
    entrada_correo.configure(width=24)
    entrada_correo.pack(expand=True, fill="x", side="left")
    grupo_correo.pack(expand=True, fill="x", padx=5, side="left")
    grupo_categoria = ttk.Frame(fila_1, name="grupo_categoria")
    etiqueta_categoria = ttk.Label(grupo_categoria, name="etiqueta_categoria")
    etiqueta_categoria.configure(text='Categoría:', width=10)
    etiqueta_categoria.pack(side="left")
    entrada_categoria = ttk.Combobox(grupo_categoria, name="entrada_categoria")
    entrada_categoria.configure(
        state="readonly",
        values='General VIP Ponente Organización',
        width=24)
    entrada_categoria.pack(expand=True, fill="x", side="left")
    grupo_categoria.pack(expand=True, fill="x", padx=5, side="left")
    fila_1.pack(fill="x", pady=5)
    registrar = ttk.Button(formulario, name="registrar")
    registrar.configure(style="success.TButton", text='Registrar Entrada')
    registrar.pack(fill="x", padx=5, pady="12 5")
    formulario.pack(fill="x")
    filtros = ttk.Frame(principal, name="filtros")
    etiqueta_buscar = ttk.Label(filtros, name="etiqueta_buscar")
    etiqueta_buscar.configure(text='Buscar:')
    etiqueta_buscar.pack(side="left")
    entrada_buscar = ttk.Entry(filtros, name="entrada_buscar")
    entrada_buscar.configure(width=28)
    entrada_buscar.pack(padx=8, side="left")
    total = ttk.Label(filtros, name="total")
    total.configure(text='Total asistentes: 0')
    total.pack(side="right")
    filtros.pack(fill="x", pady=15)
    tabla_marco = ttk.Frame(principal, name="tabla_marco")
    scroll = ttk.Scrollbar(tabla_marco, name="scroll")
    scroll.configure(orient="vertical")
    scroll.pack(fill="y", side="right")
    tabla = ttk.Treeview(tabla_marco, name="tabla")
    tabla.configure(height=10, show="headings")
    tabla_cols = [
        'id',
        'nombre',
        'apellidos',
        'correo',
        'categoria',
        'hora_entrada']
    tabla_dcols = [
        'id',
        'nombre',
        'apellidos',
        'correo',
        'categoria',
        'hora_entrada']
    tabla.configure(columns=tabla_cols, displaycolumns=tabla_dcols)
    tabla.column("id", anchor="w", stretch=True, width=45, minwidth=40)
    tabla.column("nombre", anchor="w", stretch=True, width=110, minwidth=40)
    tabla.column("apellidos", anchor="w", stretch=True, width=130, minwidth=40)
    tabla.column("correo", anchor="w", stretch=True, width=190, minwidth=40)
    tabla.column("categoria", anchor="w", stretch=True, width=105, minwidth=40)
    tabla.column(
        "hora_entrada",
        anchor="w",
        stretch=True,
        width=165,
        minwidth=40)
    tabla.heading("id", anchor="w", text='ID')
    tabla.heading("nombre", anchor="w", text='Nombre')
    tabla.heading("apellidos", anchor="w", text='Apellidos')
    tabla.heading("correo", anchor="w", text='Correo')
    tabla.heading("categoria", anchor="w", text='Categoría')
    tabla.heading("hora_entrada", anchor="w", text='Hora de entrada')
    tabla.pack(expand=True, fill="both")
    tabla_marco.pack(expand=True, fill="both")
    acciones = ttk.Frame(principal, name="acciones")
    ver_json = ttk.Button(acciones, name="ver_json")
    ver_json.configure(text='Ver JSON')
    ver_json.pack(side="left")
    exportar = ttk.Button(acciones, name="exportar")
    exportar.configure(style="success.TButton", text='Exportar JSON…')
    exportar.pack(padx=10, side="left")
    acciones.pack(fill="x", pady="15 8")
    estado = ttk.Label(principal, name="estado")
    estado.configure(
        text='Guardado automático en asistentes.json',
        wraplength=780)
    estado.pack(anchor="w")
    principal.pack(expand=True, fill="both")

    return principal


if __name__ == "__main__":
    root = tk.Tk()
    app = nombreinicial(root)
    if isinstance(app, tk.Menu):
        root.configure(menu=app)
    root.mainloop()
