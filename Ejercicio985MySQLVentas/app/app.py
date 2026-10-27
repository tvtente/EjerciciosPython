"""Aplicación de clientes. Ejecutar con --demo para probar sin MySQL."""
import argparse
import os
import queue
import threading
import tkinter as tk
from tkinter import messagebox

import ttkbootstrap as ttk

from clientes_datos import CAMPOS, ClientesDemo, ClientesMySQL, validar_cliente


class ClientesApp(ttk.Window):
    def __init__(self, demo=False):
        super().__init__(title="Ventas · Clientes", themename="bootstrap-light", size=(1320, 980), minsize=(1000, 700))
        self.demo = demo
        self.repositorio = ClientesDemo() if demo else None
        self.seleccionado = None
        self.filas = {}
        self.ocupado = False
        self.cerrada = False
        self.eventos = queue.Queue()
        self.controles = []
        self.busqueda = tk.StringVar()
        self.estado = tk.StringVar(value="Conecta con MySQL para cargar tus clientes.")
        self.cantidad = tk.StringVar(value="0 clientes")
        self.id_texto = tk.StringVar(value="Nuevo cliente")
        self.campos = {campo: tk.StringVar() for campo in CAMPOS}
        self.config = {k: tk.StringVar(value=v) for k, v in {
            "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
            "port": os.getenv("MYSQL_PORT", "3306"),
            "user": os.getenv("MYSQL_USER", "root"),
            "database": os.getenv("MYSQL_DATABASE", "ventas"),
            "password": os.getenv("MYSQL_PASSWORD", "@ng3lBTeVeTD"),
        }.items()}
        self._interfaz()
        self._ajustar_tamano()
        self.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.bind("<Control-f>", lambda _e: self.entrada_busqueda.focus_set())
        self.bind("<Control-n>", lambda _e: self.nuevo())
        self._temporizador = self.after(80, self._recoger_eventos)
        if demo:
            self.estado.set("Modo demostración · Los cambios solo existen en memoria.")
            self._mostrar(self.repositorio.listar())
        self._botones()

    def _ajustar_tamano(self):
        """Dar más espacio vertical sin colocar la ventana fuera de la pantalla."""
        self.update_idletasks()
        ancho_disponible = max(1, self.winfo_screenwidth() - 40)
        alto_disponible = max(1, self.winfo_screenheight() - 90)
        ancho = min(max(1320, self.winfo_reqwidth()), ancho_disponible)
        alto = min(max(980, self.winfo_reqheight() + 30), alto_disponible)
        self.minsize(min(1000, ancho), min(880, alto))
        self.geometry(f"{ancho}x{alto}+20+20")

    def _interfaz(self):
        contenedor = ttk.Frame(self, padding=22)
        contenedor.pack(fill="both", expand=True)
        cabecera = ttk.Frame(contenedor)
        cabecera.pack(fill="x", pady=(0, 16))
        ttk.Label(cabecera, text="Clientes", font=("TkDefaultFont", 24, "bold")).pack(side="left")
        ttk.Label(cabecera, text="VENTAS / AGENDA", bootstyle="secondary").pack(side="right")
        ttk.Label(contenedor, text="Consulta tu agenda y gestiona los datos de cada cliente.", bootstyle="secondary").pack(anchor="w", pady=(0, 16))

        conexion = ttk.Labelframe(contenedor, text=" Conexión MySQL ", padding=12)
        conexion.pack(fill="x", pady=(0, 18))
        for col, (clave, etiqueta, ancho) in enumerate([
            ("host", "Servidor", 17), ("port", "Puerto", 7), ("database", "Base de datos", 16),
            ("user", "Usuario", 13), ("password", "Contraseña", 18),
        ]):
            ttk.Label(conexion, text=etiqueta, bootstyle="secondary").grid(row=0, column=col, sticky="w", padx=5)
            entrada = ttk.Entry(conexion, textvariable=self.config[clave], width=ancho, show="•" if clave == "password" else "")
            entrada.grid(row=1, column=col, sticky="ew", padx=5, pady=(5, 0))
            conexion.columnconfigure(col, weight=1 if clave in ("host", "database", "password") else 0)
            self.controles.append(entrada)
        self.conectar_btn = ttk.Button(conexion, text="Conectar", command=self.conectar, bootstyle="primary")
        self.conectar_btn.grid(row=1, column=5, padx=(12, 0))
        self.controles.append(self.conectar_btn)
        if self.demo:
            ttk.Label(conexion, text="DEMO: conexión desactivada", bootstyle="warning").grid(row=2, column=0, columnspan=6, sticky="w", pady=(8, 0))

        cuerpo = ttk.Frame(contenedor)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.columnconfigure(0, weight=3)
        cuerpo.columnconfigure(1, weight=1, minsize=300)
        cuerpo.rowconfigure(0, weight=1)
        lista = ttk.Frame(cuerpo)
        lista.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        barra = ttk.Frame(lista)
        barra.pack(fill="x", pady=(0, 10))
        self.entrada_busqueda = ttk.Entry(barra, textvariable=self.busqueda)
        self.entrada_busqueda.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.entrada_busqueda.bind("<Return>", lambda _e: self.buscar())
        self.buscar_btn = ttk.Button(barra, text="Buscar", command=self.buscar, bootstyle="primary outline")
        self.buscar_btn.pack(side="left", padx=(0, 6))
        self.todos_btn = ttk.Button(barra, text="Ver todos", command=self.ver_todos, bootstyle="secondary outline")
        self.todos_btn.pack(side="left")
        self.controles.extend([self.entrada_busqueda, self.buscar_btn, self.todos_btn])
        ttk.Label(lista, text="Busca por ID, nombre o apellidos · Selecciona una fila para editar.", bootstyle="secondary", wraplength=620).pack(anchor="w", pady=(0, 10))
        tabla_frame = ttk.Frame(lista)
        tabla_frame.pack(fill="both", expand=True)
        columnas = ("idCliente",) + CAMPOS
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", selectmode="browse", height=14, bootstyle="primary")
        titulos = ("ID", "Nombre", "Primer apellido", "Segundo apellido", "Ciudad", "Categoría")
        for campo, titulo in zip(columnas, titulos):
            self.tabla.heading(campo, text=titulo)
            self.tabla.column(campo, width=65 if campo in ("idCliente", "Categoria") else 125, minwidth=55, stretch=True)
        vertical = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla.yview)
        horizontal = ttk.Scrollbar(tabla_frame, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        self.tabla.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        tabla_frame.rowconfigure(0, weight=1)
        tabla_frame.columnconfigure(0, weight=1)
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar)
        ttk.Label(lista, textvariable=self.cantidad, bootstyle="secondary").pack(anchor="w", pady=(8, 0))

        formulario = ttk.Labelframe(cuerpo, text=" Datos del cliente ", padding=16)
        formulario.grid(row=0, column=1, sticky="nsew")
        ttk.Label(formulario, textvariable=self.id_texto, font=("TkDefaultFont", 12, "bold"), bootstyle="primary").pack(anchor="w", pady=(0, 10))
        for campo, titulo in zip(CAMPOS, ("Nombre *", "Primer apellido *", "Segundo apellido", "Ciudad", "Categoría")):
            ttk.Label(formulario, text=titulo).pack(anchor="w", pady=(8, 3))
            entrada = ttk.Entry(formulario, textvariable=self.campos[campo])
            entrada.pack(fill="x")
            self.controles.append(entrada)
        ttk.Label(formulario, text="* Obligatorio. Categoría: entero ≥ 0 o vacío.", wraplength=270, bootstyle="secondary").pack(anchor="w", pady=(10, 14))
        self.guardar_btn = ttk.Button(formulario, text="Crear cliente", command=self.guardar, bootstyle="success")
        self.guardar_btn.pack(fill="x", pady=(0, 7))
        self.nuevo_btn = ttk.Button(formulario, text="Nuevo / limpiar", command=self.nuevo, bootstyle="secondary outline")
        self.nuevo_btn.pack(fill="x", pady=(0, 7))
        self.eliminar_btn = ttk.Button(formulario, text="Eliminar cliente", command=self.eliminar, bootstyle="danger outline")
        self.eliminar_btn.pack(fill="x")
        self.controles.extend([self.guardar_btn, self.nuevo_btn, self.eliminar_btn])
        ttk.Separator(contenedor).pack(fill="x", pady=(16, 10))
        ttk.Label(contenedor, textvariable=self.estado, bootstyle="secondary", wraplength=1100).pack(anchor="w")

    def _botones(self):
        for widget in self.controles:
            widget.configure(state="disabled" if self.ocupado else "normal")
        if self.demo:
            for child in self.conectar_btn.master.winfo_children():
                if child.winfo_class() in ("TEntry", "TButton"):
                    child.configure(state="disabled")
        if self.repositorio is None or self.ocupado:
            for widget in [self.buscar_btn, self.todos_btn, self.guardar_btn, self.nuevo_btn, self.eliminar_btn]:
                widget.configure(state="disabled")
        elif self.seleccionado is None:
            self.eliminar_btn.configure(state="disabled")
        self.guardar_btn.configure(text="Guardar cambios" if self.seleccionado is not None else "Crear cliente")

    def _trabajar(self, texto, operacion, al_terminar):
        if self.ocupado:
            return
        self.ocupado = True
        self.estado.set(texto)
        self._botones()
        def ejecutar():
            try:
                self.eventos.put((True, operacion(), al_terminar))
            except Exception as error:
                self.eventos.put((False, error, al_terminar))
        threading.Thread(target=ejecutar, daemon=True).start()

    def _recoger_eventos(self):
        if self.cerrada:
            return
        try:
            correcto, resultado, callback = self.eventos.get_nowait()
        except queue.Empty:
            pass
        else:
            self.ocupado = False
            if correcto:
                callback(resultado)
            else:
                self.estado.set("No se pudo completar la operación.")
                messagebox.showerror("Operación no completada", str(resultado), parent=self)
            self._botones()
        self._temporizador = self.after(80, self._recoger_eventos)

    def conectar(self):
        if self.ocupado or self.demo:
            return
        datos = {k: v.get().strip() if k != "password" else v.get() for k, v in self.config.items()}
        try:
            datos["port"] = int(datos["port"])
            if not 1 <= datos["port"] <= 65535 or not all(datos[k] for k in ("host", "user", "database")):
                raise ValueError
        except ValueError:
            messagebox.showerror("Datos de conexión", "Indica servidor, usuario, base y un puerto entre 1 y 65535.", parent=self)
            return
        repo = ClientesMySQL(datos)
        self.repositorio = None
        self._mostrar([])
        self.nuevo()
        def listo(filas):
            self.repositorio = repo
            self.busqueda.set("")
            self._mostrar(filas)
            self.estado.set(f"Conectado a {datos['host']}:{datos['port']} / {datos['database']}.")
        self._trabajar("Conectando con MySQL…", repo.listar, listo)

    def _mostrar(self, filas):
        self.filas = {fila["idCliente"]: fila for fila in filas}
        hijos = self.tabla.get_children()
        if hijos:
            self.tabla.delete(*hijos)
        for fila in filas:
            self.tabla.insert("", "end", iid=str(fila["idCliente"]), values=["" if fila.get(c) is None else fila[c] for c in ("idCliente",) + CAMPOS])
        self.cantidad.set(f"{len(filas)} cliente{'s' if len(filas) != 1 else ''}")

    def _seleccionar(self, _evento=None):
        if self.ocupado:
            return
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        fila = self.filas.get(int(seleccion[0]))
        if fila is None:
            return
        self.seleccionado = fila["idCliente"]
        self.id_texto.set(f"Cliente #{self.seleccionado}")
        for campo, variable in self.campos.items():
            variable.set("" if fila[campo] is None else str(fila[campo]))
        self._botones()

    def nuevo(self):
        if self.ocupado:
            return
        self.seleccionado = None
        self.id_texto.set("Nuevo cliente")
        for variable in self.campos.values():
            variable.set("")
        seleccion = self.tabla.selection()
        if seleccion:
            self.tabla.selection_remove(*seleccion)
        self._botones()

    def buscar(self):
        if self.repositorio is None or self.ocupado:
            return
        repo, texto = self.repositorio, self.busqueda.get()
        def listo(filas):
            self.nuevo()
            self._mostrar(filas)
            self.estado.set("Búsqueda completada." if filas else "No hay clientes que coincidan. Prueba otro nombre o ID.")
        self._trabajar("Buscando clientes…", lambda: repo.listar(texto), listo)

    def ver_todos(self):
        if not self.ocupado:
            self.busqueda.set("")
            self.buscar()

    def guardar(self):
        if self.repositorio is None or self.ocupado:
            return
        try:
            datos = validar_cliente({k: v.get() for k, v in self.campos.items()})
        except ValueError as error:
            messagebox.showerror("Revisa el formulario", str(error), parent=self)
            return
        repo, cliente_id = self.repositorio, self.seleccionado
        # Refrescar es una operación separada: si falla tras el commit, informar
        # de que el guardado sí se realizó, para evitar duplicar una inserción.
        self._trabajar("Guardando cliente…", lambda: repo.guardar(cliente_id, datos), self._guardado)

    def _guardado(self, cliente_id):
        self.nuevo()
        self.busqueda.set("")
        self.estado.set(f"Cliente #{cliente_id} guardado. Pulsa Ver todos para actualizar la lista.")
        messagebox.showinfo("Cliente guardado", f"Se ha guardado el cliente #{cliente_id}.", parent=self)
        self.ver_todos()

    def eliminar(self):
        if self.repositorio is None or self.ocupado or self.seleccionado is None:
            return
        cliente_id = self.seleccionado
        texto = f"¿Eliminar al cliente #{cliente_id}?\n\nEn el esquema ventas, sus pedidos también se eliminan por ON DELETE CASCADE. Esta acción no se puede deshacer."
        if not messagebox.askyesno("Eliminar cliente", texto, parent=self, default="no"):
            return
        repo = self.repositorio
        def listo(_resultado):
            self.nuevo()
            self.estado.set(f"Cliente #{cliente_id} eliminado.")
            self.ver_todos()
        self._trabajar("Eliminando cliente…", lambda: repo.eliminar(cliente_id), listo)

    def cerrar(self):
        if self.ocupado:
            messagebox.showinfo("Operación en curso", "Espera a que termine la operación antes de cerrar.", parent=self)
            return
        self.cerrada = True
        self.after_cancel(self._temporizador)
        self.destroy()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true", help="Abrir con datos de ejemplo en memoria")
    args = parser.parse_args()
    ClientesApp(demo=args.demo).mainloop()


if __name__ == "__main__":
    main()
