"""Ejemplo: una ventana con un tema cargado desde JSON."""

from pathlib import Path
import ttkbootstrap as ttk


def main():
    # Window crea la única ventana principal y su estilo.
    ventana = ttk.Window(title="Mi aplicación con tema personalizado")
    ventana.geometry("500x320")

    # La ruta funciona aunque ejecutes el programa desde otra carpeta.
    archivo_tema = Path(__file__).parent / "json" / "my_themes.json"
    style = ventana.style
    style.load_user_themes(str(archivo_tema))
    style.theme_use("custom_name")

    contenido = ttk.Frame(ventana, padding=25)
    contenido.pack(fill="both", expand=True)

    ttk.Label(contenido, text="Mi tema personalizado", font=("Sans", 18)).pack(
        anchor="w", pady=(0, 15)
    )
    ttk.Label(contenido, text="¿Cómo te llamas?").pack(anchor="w")
    nombre = ttk.Entry(contenido)
    nombre.pack(fill="x", pady=10)

    mensaje = ttk.Label(contenido, text="Los colores vienen del archivo JSON.")
    mensaje.pack(anchor="w", pady=10)

    def saludar():
        texto = nombre.get().strip()
        mensaje.configure(text=f"¡Hola, {texto}!" if texto else "Escribe tu nombre.")

    botones = ttk.Frame(contenido)
    botones.pack(anchor="w", pady=10)
    ttk.Button(botones, text="Saludar", bootstyle="success", command=saludar).pack(
        side="left", padx=(0, 10)
    )
    ttk.Button(
        botones, text="Salir", bootstyle="danger-outline", command=ventana.destroy
    ).pack(side="left")

    nombre.focus_set()
    ventana.mainloop()


if __name__ == "__main__":
    main()
