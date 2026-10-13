import json
import os
from datetime import datetime
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

# Nombre del archivo JSON donde se guardarán los datos
JSON_FILE = "asistentes.json"

class ControlAccesoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Control de Acceso a Eventos")
        self.root.geometry("850x600")
        self.root.minsize(750, 500)

        # Cargar datos existentes si el archivo JSON ya existe
        self.asistentes = self.cargar_datos()

        # --- CONTENEDOR PRINCIPAL ---
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)

        # Título de la aplicación
        titulo = ttk.Label(
            main_frame, 
            text="Control de Entrada a Evento", 
            font=("Helvetica", 18, "bold"), 
            bootstyle="primary"
        )
        titulo.pack(pady=(0, 15))

        # --- SECCIÓN DE FORMULARIO (IZQUIERDA/ARRIBA) ---
        form_frame = ttk.LabelFrame(main_frame, text=" Registrar Nuevo Asistente ", padding=15, bootstyle="info")
        form_frame.pack(fill=X, padx=5, pady=5)

        # Usamos una cuadrícula (grid) para organizar los campos
        # Nombre
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.entry_nombre = ttk.Entry(form_frame, width=25)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        # Apellidos
        ttk.Label(form_frame, text="Apellidos:").grid(row=0, column=2, sticky=W, padx=5, pady=5)
        self.entry_apellidos = ttk.Entry(form_frame, width=25)
        self.entry_apellidos.grid(row=0, column=3, padx=5, pady=5)

        # Correo Electrónico
        ttk.Label(form_frame, text="Correo:").grid(row=1, column=0, sticky=W, padx=5, pady=5)
        self.entry_correo = ttk.Entry(form_frame, width=25)
        self.entry_correo.grid(row=1, column=1, padx=5, pady=5)

        # Tipo de Entrada / Categoría
        ttk.Label(form_frame, text="Categoría:").grid(row=1, column=2, sticky=W, padx=5, pady=5)
        self.combo_categoria = ttk.Combobox(
            form_frame, 
            values=["General", "VIP", "Prensa", "Ponente", "Staff"], 
            width=23, 
            state="readonly"
        )
        self.combo_categoria.grid(row=1, column=3, padx=5, pady=5)
        self.combo_categoria.set("General") # Valor por defecto

        # Botón de Registro
        btn_registrar = ttk.Button(
            form_frame, 
            text="Registrar Entrada", 
            command=self.registrar_asistente, 
            bootstyle="success"
        )
        btn_registrar.grid(row=2, column=0, columnspan=4, pady=15, sticky=EW)

        # --- SECCIÓN DE BÚSQUEDA Y TABLA ---
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=X, padx=5, pady=(15, 5))

        ttk.Label(search_frame, text="Buscar:", font=("Helvetica", 10, "bold")).pack(side=LEFT, padx=(0, 5))
        self.entry_buscar = ttk.Entry(search_frame, width=30)
        self.entry_buscar.pack(side=LEFT, padx=5)
        self.entry_buscar.bind("<KeyRelease>", self.filtrar_tabla)

        # Contador de asistentes
        self.lbl_contador = ttk.Label(search_frame, text="", font=("Helvetica", 10, "bold"), bootstyle="secondary")
        self.lbl_contador.pack(side=RIGHT, padx=5)

        # Tabla de Registros (Treeview)
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=BOTH, expand=YES, padx=5, pady=5)

        columnas = ("id", "nombre", "apellidos", "correo", "categoria", "hora")
        self.tabla = ttk.Treeview(table_frame, columns=columnas, show="headings", bootstyle="info")

        # Definir cabeceras de la tabla
        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("apellidos", text="Apellidos")
        self.tabla.heading("correo", text="Correo")
        self.tabla.heading("categoria", text="Categoría")
        self.tabla.heading("hora", text="Hora de Entrada")

        # Definir anchos de columna
        self.tabla.column("id", width=40, anchor=CENTER)
        self.tabla.column("nombre", width=120, anchor=W)
        self.tabla.column("apellidos", width=140, anchor=W)
        self.tabla.column("correo", width=180, anchor=W)
        self.tabla.column("categoria", width=100, anchor=CENTER)
        self.tabla.column("hora", width=130, anchor=CENTER)

        # Barra de desplazamiento para la tabla
        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Cargar los datos iniciales en la tabla y actualizar contador
        self.actualizar_tabla(self.asistentes)

    def cargar_datos(self):
        """Carga los datos desde el archivo JSON si existe."""
        if os.path.exists(JSON_FILE):
            try:
                with open(JSON_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo JSON:\n{e}")
                return []
        return []

    def guardar_datos(self):
        """Guarda la lista completa de asistentes en el archivo JSON."""
        try:
            with open(JSON_FILE, "w", encoding="utf-8") as f:
                json.dump(self.asistentes, f, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo JSON:\n{e}")

    def registrar_asistente(self):
        """Valida el formulario, añade el asistente y lo guarda."""
        nombre = self.entry_nombre.get().strip()
        apellidos = self.entry_apellidos.get().strip()
        correo = self.entry_correo.get().strip()
        categoria = self.combo_categoria.get()

        # Validación simple de campos obligatorios
        if not nombre or not apellidos or not correo:
            messagebox.showwarning("Campos vacíos", "Por favor completa Nombre, Apellidos y Correo.")
            return

        # Generar ID único incremental y hora actual
        nuevo_id = len(self.asistentes) + 1
        hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        nuevo_registro = {
            "id": nuevo_id,
            "nombre": nombre,
            "apellidos": apellidos,
            "correo": correo,
            "categoria": categoria,
            "hora": hora_actual
        }

        # Añadir a la lista y guardar en JSON
        self.asistentes.append(nuevo_registro)
        self.guardar_datos()

        # Actualizar vista y limpiar campos
        self.actualizar_tabla(self.asistentes)
        self.limpiar_formulario()

        messagebox.showinfo("Éxito", f"¡Asistente {nombre} registrado correctamente!")

    def actualizar_tabla(self, lista_asistentes):
        """Limpia la tabla y vuelve a insertar los elementos dados."""
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for a in lista_asistentes:
            self.tabla.insert("", END, values=(a["id"], a["nombre"], a["apellidos"], a["correo"], a["categoria"], a["hora"]))

        # Actualizar texto del contador
        total = len(self.asistentes)
        registrados_filtrados = len(lista_asistentes)
        if total == registrados_filtrados:
            self.lbl_contador.config(text=f"Total Asistentes: {total}")
        else:
            self.lbl_contador.config(text=f"Mostrando: {registrados_filtrados} de {total}")

    def filtrar_tabla(self, event):
        """Filtra la tabla en tiempo real según lo escrito en el buscador."""
        texto_busqueda = self.entry_buscar.get().lower()
        if not texto_busqueda:
            self.actualizar_tabla(self.asistentes)
            return

        filtrados = [
            a for a in self.asistentes 
            if texto_busqueda in a["nombre"].lower() 
            or texto_busqueda in a["apellidos"].lower() 
            or texto_busqueda in a["correo"].lower()
            or texto_busqueda in a["categoria"].lower()
        ]
        self.actualizar_tabla(filtrados)

    def limpiar_formulario(self):
        """Limpia las entradas del formulario tras un registro exitoso."""
        self.entry_nombre.delete(0, END)
        self.entry_apellidos.delete(0, END)
        self.entry_correo.delete(0, END)
        self.combo_categoria.set("General")
        self.entry_nombre.focus()

if __name__ == "__main__":
    # Usamos un tema moderno de ttkbootstrap (ej. 'cosmo', 'flatly', 'journal', 'superhero')
    app = ttk.Window(themename="flatly")
    ControlAccesoApp(app)
    app.mainloop()