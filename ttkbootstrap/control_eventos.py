"""Registro de asistentes: ejecutar con python3 control_eventos.py."""

import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from tkinter import StringVar, Text, filedialog, messagebox

import ttkbootstrap as ttk


ARCHIVO = Path(__file__).with_name("asistentes.json")
CATEGORIAS = ("General", "VIP", "Prensa", "Ponente", "Organización")
CAMPOS = ("id", "nombre", "apellidos", "correo", "categoria", "hora_entrada")


@dataclass
class Persona:
    """Un asistente del evento. dataclass genera el constructor __init__."""

    id: int
    nombre: str
    apellidos: str
    correo: str
    categoria: str
    hora_entrada: str

    def a_diccionario(self):
        """JSON necesita datos simples: convertimos el objeto a diccionario."""
        return asdict(self)

    def a_fila(self):
        """Valores en el mismo orden que las columnas de la tabla."""
        return (self.id, self.nombre, self.apellidos, self.correo,
                self.categoria, self.hora_entrada)

    @classmethod
    def desde_diccionario(cls, registro):
        """Valida un registro leído del JSON y construye una Persona."""
        if not isinstance(registro, dict) or not all(c in registro for c in CAMPOS):
            raise ValueError("Hay un registro incompleto en el JSON.")
        if type(registro["id"]) is not int or registro["id"] < 1:
            raise ValueError("El identificador debe ser un entero positivo.")
        if not all(isinstance(registro[c], str) for c in CAMPOS[1:]):
            raise ValueError("Los campos del asistente deben contener texto.")
        return cls(
            id=registro["id"],
            nombre=registro["nombre"],
            apellidos=registro["apellidos"],
            correo=registro["correo"],
            categoria=registro["categoria"],
            hora_entrada=registro["hora_entrada"],
        )


def cargar_datos(ruta):
    if not ruta.exists():
        return []
    registros = json.loads(ruta.read_text(encoding="utf-8"))
    if not isinstance(registros, list):
        raise ValueError("El JSON debe contener una lista de asistentes.")
    personas = []
    ids = set()
    for registro in registros:
        persona = Persona.desde_diccionario(registro)
        if persona.id in ids:
            raise ValueError("Los identificadores deben ser únicos.")
        ids.add(persona.id)
        personas.append(persona)
    return personas


def convertir_a_json(personas):
    registros = [persona.a_diccionario() for persona in personas]
    return json.dumps(registros, ensure_ascii=False, indent=2)


def guardar_datos(ruta, personas):
    # Primero escribimos un temporal y después reemplazamos el archivo completo.
    temporal = ruta.with_name(ruta.name + ".tmp")
    registros = [persona.a_diccionario() for persona in personas]
    with temporal.open("w", encoding="utf-8") as archivo:
        json.dump(registros, archivo, ensure_ascii=False, indent=2)
        archivo.write("\n")
    temporal.replace(ruta)


class ControlEventos:
    def __init__(self, ventana, datos):
        self.ventana = ventana
        self.datos = datos
        self.campos = {c: StringVar(master=ventana) for c in CAMPOS[1:5]}
        self.campos["categoria"].set("General")
        self.busqueda = StringVar(master=ventana)
        self.estado = StringVar(master=ventana, value=f"Guardado automático: {ARCHIVO.name}")

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
        self.total = ttk.Label(filtros)
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

    def registrar_asistente(self):
        valores = {campo: variable.get().strip() for campo, variable in self.campos.items()}
        if not all(valores.values()):
            messagebox.showwarning("Faltan datos", "Completa todos los campos.", parent=self.ventana)
            return
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", valores["correo"]):
            messagebox.showwarning("Correo incorrecto", "Escribe un correo como nombre@ejemplo.com.",
                                    parent=self.ventana)
            return
        # Aquí creamos un objeto de nuestra clase Persona.
        persona = Persona(
            id=max((p.id for p in self.datos), default=0) + 1,
            nombre=valores["nombre"],
            apellidos=valores["apellidos"],
            correo=valores["correo"],
            categoria=valores["categoria"],
            hora_entrada=datetime.now().astimezone().isoformat(timespec="seconds"),
        )
        nuevos = self.datos + [persona]
        try:
            guardar_datos(ARCHIVO, nuevos)
        except OSError as error:
            messagebox.showerror("No se pudo guardar", str(error), parent=self.ventana)
            return
        self.datos = nuevos
        for campo in ("nombre", "apellidos", "correo"):
            self.campos[campo].set("")
        self.campos["categoria"].set("General")
        self.busqueda.set("")
        self.actualizar_tabla()
        self.estado.set(f"Entrada de {persona.nombre} guardada en {ARCHIVO.name}.")
        self.entrada_nombre.focus_set()

    def actualizar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        consulta = self.busqueda.get().strip().casefold()
        visibles = [p for p in self.datos if consulta in " ".join(str(valor) for valor in p.a_fila()).casefold()]
        for persona in visibles:
            self.tabla.insert("", "end", values=persona.a_fila())
        self.total.configure(text=f"Total asistentes: {len(self.datos)}  |  Mostrados: {len(visibles)}")

    def ver_json(self):
        visor = ttk.Toplevel(master=self.ventana, title="Datos guardados en JSON")
        visor.geometry("760x480")
        texto = Text(visor, wrap="word", padx=12, pady=12)
        scroll = ttk.Scrollbar(visor, command=texto.yview)
        scroll.pack(side="right", fill="y")
        texto.configure(yscrollcommand=scroll.set)
        texto.pack(fill="both", expand=True)
        texto.insert("1.0", convertir_a_json(self.datos))
        texto.configure(state="disabled")

    def exportar(self):
        destino = filedialog.asksaveasfilename(parent=self.ventana, title="Exportar todos los asistentes",
                                                initialfile="asistentes_exportados.json",
                                                defaultextension=".json",
                                                filetypes=[("Archivo JSON", "*.json")])
        if not destino:
            return
        try:
            guardar_datos(Path(destino), self.datos)
        except OSError as error:
            messagebox.showerror("Error al exportar", str(error), parent=self.ventana)
            return
        self.estado.set(f"JSON exportado en: {destino}")


def main():
    ventana = ttk.Window(title="Control de Acceso a Eventos", themename="flatly")
    ventana.geometry("900x620")
    ventana.minsize(820, 560)
    try:
        datos = cargar_datos(ARCHIVO)
    except (OSError, ValueError) as error:
        messagebox.showerror("No se pudo leer asistentes.json",
                                f"El archivo se conserva sin cambios.\n\n{error}", parent=ventana)
        ventana.destroy()
        return
    ControlEventos(ventana, datos)
    ventana.mainloop()


if __name__ == "__main__":
    main()
