"""Interfaz sin lógica de negocio, equivalente a una base de diseñador.

Ejecutar: python3 control_eventos.py
Versión completa: control_eventos_funcional.py.
Esta base no lee ni modifica asistentes.json. No es una exportación de Pygubu.
"""

from tkinter import StringVar

import ttkbootstrap as ttk


CATEGORIAS = ("General", "VIP", "Prensa", "Ponente", "Organización")
CAMPOS = ("id", "nombre", "apellidos", "correo", "categoria", "hora_entrada")


class ControlEventos:
    def __init__(self, ventana):
        self.ventana = ventana
        self.campos = {c: StringVar(master=ventana) for c in CAMPOS[1:5]}
        self.campos["categoria"].set("General")
        self.busqueda = StringVar(master=ventana)
        self.estado = StringVar(master=ventana, value="Diseño del formulario: acciones pendientes de programar.")

        contenido = ttk.Frame(ventana, padding=18)
        contenido.pack(fill="both", expand=True)
        ttk.Label(contenido, text="Control de Entrada a Evento",
                  font=("Sans", 20, "bold"), anchor="center").pack(fill="x", pady=(5, 20))

        formulario = ttk.Labelframe(contenido, text="Registrar Nuevo Asistente",
                                    padding=15, bootstyle="info")
        formulario.pack(fill="x")
        # Cada fila es un contenedor; usamos pack para colocar sus elementos.
        for pares in ((('nombre', 'Nombre:'), ('apellidos', 'Apellidos:')),
                        (('correo', 'Correo:'), ('categoria', 'Categoría:'))):
            fila = ttk.Frame(formulario)
            fila.pack(fill="x", pady=5)
            for campo, titulo in pares:
                grupo = ttk.Frame(fila)
                grupo.pack(side="left", fill="x", expand=True, padx=5)
                ttk.Label(grupo, text=titulo, width=10).pack(side="left")
                if campo == "categoria":
                    control = ttk.Combobox(grupo, textvariable=self.campos[campo],
                                            values=CATEGORIAS, state="readonly", width=22)
                else:
                    control = ttk.Entry(grupo, textvariable=self.campos[campo], width=24)
                control.pack(side="left", fill="x", expand=True)
                if campo == "nombre":
                    self.entrada_nombre = control
        ttk.Button(formulario, text="Registrar Entrada", bootstyle="success",
                    command=self.registrar_asistente).pack(fill="x", padx=5, pady=(12, 5))

        filtros = ttk.Frame(contenido)
        filtros.pack(fill="x", pady=15)
        ttk.Label(filtros, text="Buscar:", font=("Sans", 10, "bold")).pack(side="left")
        ttk.Entry(filtros, textvariable=self.busqueda, width=28).pack(side="left", padx=8)
        self.total = ttk.Label(filtros, text="Total asistentes: 0  |  Mostrados: 0")
        self.total.pack(side="right")

        tabla_marco = ttk.Frame(contenido)
        tabla_marco.pack(fill="both", expand=True)
        self.tabla = ttk.Treeview(tabla_marco, columns=CAMPOS, show="headings",
                                    bootstyle="info", height=10)
        titulos = ("ID", "Nombre", "Apellidos", "Correo", "Categoría", "Hora de entrada")
        anchos = (45, 110, 130, 190, 105, 165)
        for campo, titulo, ancho in zip(CAMPOS, titulos, anchos):
            self.tabla.heading(campo, text=titulo)
            self.tabla.column(campo, width=ancho, minwidth=40, stretch=True)
        scroll = ttk.Scrollbar(tabla_marco, orient="vertical", command=self.tabla.yview)
        scroll.pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=scroll.set)
        self.tabla.pack(fill="both", expand=True)

        acciones = ttk.Frame(contenido)
        acciones.pack(fill="x", pady=(15, 8))
        ttk.Button(acciones, text="Ver JSON", command=self.ver_json,
                    bootstyle="info-outline").pack(side="left")
        ttk.Button(acciones, text="Exportar JSON…", command=self.exportar,
                    bootstyle="success").pack(side="left", padx=10)
        ttk.Label(contenido, textvariable=self.estado, wraplength=780).pack(anchor="w")
        self.busqueda.trace_add("write", lambda *_: self.actualizar_tabla())
        self.actualizar_tabla()
        self.entrada_nombre.focus_set()

    # Puntos de conexión para añadir la lógica después del diseño.
    def registrar_asistente(self):
        # Pendiente: validar, crear Persona, guardar JSON y limpiar formulario.
        pass

    def actualizar_tabla(self):
        # Pendiente: filtrar asistentes y actualizar filas y contador.
        pass

    def ver_json(self):
        # Pendiente: mostrar los datos guardados.
        pass

    def exportar(self):
        # Pendiente: elegir un destino y exportar los asistentes.
        pass


def main():
    ventana = ttk.Window(title="Control de Acceso a Eventos", themename="flatly")
    ventana.geometry("900x620")
    ventana.minsize(820, 560)
    ControlEventos(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    main()
