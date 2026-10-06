"""Primer ejemplo de una ventana con ttkbootstrap."""

import ttkbootstrap as ttk


def main():
    # 1. Creamos una única ventana principal; Window también crea su estilo.
    ventana = ttk.Window(
        title="Mi primera ventana",
        themename="darkly"
    )
    ventana.geometry("440x260")  # Ancho x alto, en píxeles.
    ventana.resizable(False, False)

    # 2. Un Frame agrupa los elementos y deja margen alrededor.
    contenido = ttk.Frame(ventana, padding=25)
    contenido.pack(fill="both", expand=True)

    # 3. Label muestra texto y Entry permite escribir.
    ttk.Label(contenido, text="Escribe tu nombre:").pack(anchor="w")
    entrada_nombre = ttk.Entry(contenido)
    entrada_nombre.pack(fill="x", pady=(8, 15))

    resultado = ttk.Label(contenido, text="¡Bienvenido al curso de Python!")
    resultado.pack(pady=(0, 20))

    # 4. Esta función se ejecuta al pulsar el botón Saludar.
    def saludar():
        nombre = entrada_nombre.get().strip()
        if nombre:
            resultado.config(text=f"¡Hola, {nombre}!")
        else:
            resultado.config(text="Por favor, escribe tu nombre.")

    botones = ttk.Frame(contenido)
    botones.pack()
    ttk.Button(botones, text="Saludar", style='success.TButton',command=saludar).pack(
        side="left", padx=5
    )
    ttk.Button(botones, text="Salir", style='success.Outline.TButton', command=ventana.destroy).pack(
        side="left", padx=5
    )

    entrada_nombre.focus_set()

    # 5. Mantiene la ventana abierta y escucha clics y pulsaciones.
    ventana.mainloop()


if __name__ == "__main__":
    main()
