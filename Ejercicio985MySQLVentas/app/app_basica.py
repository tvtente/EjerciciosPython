"""CRUD básico: funciones, formulario y botones. Sin hilos ni clases propias."""
from pathlib import Path
import sys
from tkinter import messagebox

import ttkbootstrap as ttk
from mysql.connector import Error

# Permite importar los archivos de la carpeta db.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "db"))
from conexion_mysql import conectar
from consultar_cliente import consultar_clientes
from insertar_cliente import insertar_cliente
from actualizar_cliente import actualizar_cliente_completo
from eliminar_cliente import eliminar_cliente


# 1. FUNCIONES QUE EJECUTAN LOS BOTONES

def listar():
    try:
        clientes = consultar_clientes(conexion)
        for fila in tabla.get_children():
            tabla.delete(fila)
        for cliente in clientes:
            valores = [cliente[campo] if cliente[campo] is not None else "" for campo in columnas]
            tabla.insert("", "end", iid=str(cliente["idCliente"]), values=valores)
        estado.configure(text=f"{len(clientes)} clientes")
    except Error as error:
        messagebox.showerror("Error al consultar", str(error))


def limpiar():
    global id_seleccionado
    id_seleccionado = None
    for entrada in entradas:
        entrada.delete(0, "end")
    seleccion = tabla.selection()
    if seleccion:
        tabla.selection_remove(*seleccion)
    estado.configure(text="Nuevo cliente: completa los datos y pulsa Insertar.")


def seleccionar(evento):
    global id_seleccionado
    seleccion = tabla.selection()
    if not seleccion:
        return
    id_seleccionado = int(seleccion[0])
    valores = tabla.item(seleccion[0], "values")
    for entrada, valor in zip(entradas, valores[1:]):
        entrada.delete(0, "end")
        entrada.insert(0, valor)
    estado.configure(text=f"Cliente seleccionado: {id_seleccionado}")


def leer_formulario():
    nombre, apellido1, apellido2, ciudad, categoria = [e.get().strip() for e in entradas]
    if not nombre or not apellido1:
        raise ValueError("Nombre y primer apellido son obligatorios.")
    if any(len(texto) > limite for texto, limite in
           ((nombre, 25), (apellido1, 25), (apellido2, 25), (ciudad, 35))):
        raise ValueError("Nombre y apellidos: máximo 25 caracteres. Ciudad: máximo 35.")
    categoria = int(categoria) if categoria else None
    if categoria is not None and not 0 <= categoria <= 4294967295:
        raise ValueError("La categoría debe ser un entero no negativo.")
    return nombre, apellido1, apellido2 or None, ciudad or None, categoria


def crear():
    try:
        datos = leer_formulario()
        nuevo_id = insertar_cliente(conexion, *datos)
        conexion.commit()
    except (Error, ValueError) as error:
        conexion.rollback()
        messagebox.showerror("No se pudo insertar", str(error))
        return
    limpiar()
    listar()
    estado.configure(text=f"Cliente creado con ID {nuevo_id}.")


def actualizar():
    if id_seleccionado is None:
        messagebox.showinfo("Selecciona un cliente", "Pulsa una fila de la tabla antes de actualizar.")
        return
    try:
        datos = leer_formulario()
        encontrado = actualizar_cliente_completo(conexion, id_seleccionado, *datos)
        conexion.commit()
    except (Error, ValueError) as error:
        conexion.rollback()
        messagebox.showerror("No se pudo actualizar", str(error))
        return
    limpiar()
    listar()
    estado.configure(text="Cliente actualizado." if encontrado else "El cliente ya no existe.")


def eliminar():
    if id_seleccionado is None:
        messagebox.showinfo("Selecciona un cliente", "Pulsa una fila de la tabla antes de eliminar.")
        return
    if not messagebox.askyesno(
        "Eliminar cliente",
        f"¿Eliminar el cliente {id_seleccionado}? También se borrarán sus pedidos.",
        default="no",
    ):
        return
    try:
        eliminado = eliminar_cliente(conexion, id_seleccionado)
        conexion.commit()
    except Error as error:
        conexion.rollback()
        messagebox.showerror("No se pudo eliminar", str(error))
        return
    limpiar()
    listar()
    estado.configure(text="Cliente eliminado." if eliminado else "El cliente ya no existe.")


# 2. CREAR LA VENTANA Y RELACIONAR LOS BOTONES CON LAS FUNCIONES

def main():
    global conexion, ventana, tabla, entradas, columnas, id_seleccionado, estado
    try:
        # Reutiliza conexion_mysql.py; pide la contraseña en la terminal.
        conexion = conectar()
    except (Error, ValueError) as error:
        print(f"No se pudo conectar a MySQL: {error}")
        return

    try:
        id_seleccionado = None
        ventana = ttk.Window(title="Clientes · CRUD básico", themename="bootstrap-light")
        ventana.geometry("980x650")

        ttk.Label(ventana, text="Clientes", font=("TkDefaultFont", 18)).pack(pady=10)

        columnas = ("idCliente", "Nombre", "Apellido1", "Apellido2", "Ciudad", "Categoria")
        tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=10)
        for campo in columnas:
            tabla.heading(campo, text=campo)
            tabla.column(campo, width=140, minwidth=50)
        tabla.pack(fill="both", expand=True, padx=15)
        tabla.bind("<<TreeviewSelect>>", seleccionar)

        formulario = ttk.Frame(ventana, padding=15)
        formulario.pack(fill="x")
        formulario.columnconfigure(1, weight=1)
        entradas = []
        etiquetas = ("Nombre *", "Primer apellido *", "Segundo apellido", "Ciudad", "Categoría")
        for fila, etiqueta in enumerate(etiquetas):
            ttk.Label(formulario, text=etiqueta).grid(row=fila, column=0, sticky="w", pady=3)
            entrada = ttk.Entry(formulario)
            entrada.grid(row=fila, column=1, sticky="ew", padx=10, pady=3)
            entradas.append(entrada)

        botones = ttk.Frame(ventana)
        botones.pack(pady=10)
        ttk.Button(botones, text="Listar", command=listar).pack(side="left", padx=4)
        ttk.Button(botones, text="Limpiar", command=limpiar).pack(side="left", padx=4)
        ttk.Button(botones, text="Insertar", command=crear).pack(side="left", padx=4)
        ttk.Button(botones, text="Actualizar", command=actualizar).pack(side="left", padx=4)
        ttk.Button(botones, text="Eliminar", command=eliminar).pack(side="left", padx=4)

        estado = ttk.Label(ventana, text="")
        estado.pack(pady=(0, 10))
        listar()
        ventana.mainloop()
    finally:
        conexion.close()


# 3. Solo iniciar la ventana si ejecutamos este archivo directamente.
if __name__ == "__main__":
    main()
