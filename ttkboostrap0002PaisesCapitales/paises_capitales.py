"""Aplicación de países y capitales diseñada con Pygubu."""

import json
from pathlib import Path
from tkinter import messagebox

import pygubu
import ttkbootstrap as ttk


CARPETA = Path(__file__).parent
RUTA_JSON = CARPETA / "paises_capitales.json"
RUTA_UI = CARPETA / "paises_capitales.ui"


class AplicacionCapitales:
    """Conecta la pantalla de Pygubu con los datos del JSON."""

    def __init__(self):
        # ttkbootstrap proporciona el tema; Pygubu construye los controles.
        self.ventana = ttk.Window(themename="flatly")
        self.ventana.title("Países y capitales")
        self.ventana.geometry("520x330")
        self.ventana.resizable(False, False)

        self.builder = pygubu.Builder()
        self.builder.add_from_file(RUTA_UI)
        self.builder.get_object("contenedor", self.ventana)
        self.builder.connect_callbacks(self)

        # Recuperamos los controles y variables definidos en el archivo .ui.
        self.selector = self.builder.get_object("selector_pais")
        self.pais_seleccionado = self.builder.get_variable("pais_seleccionado")
        self.resultado = self.builder.get_variable("resultado")

        self.paises = self.cargar_paises()
        self.selector.configure(values=sorted(self.paises, key=str.casefold))
        self.resultado.set("Aquí aparecerá la capital")

    def cargar_paises(self):
        """Lee el JSON y devuelve un diccionario {país: capital}."""
        try:
            with RUTA_JSON.open("r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

            paises = {}
            for elemento in datos:
                # El JSON utiliza las claves country y city.
                pais = elemento.get("country")
                capital = elemento.get("city")
                if pais and capital:
                    paises[pais] = capital
            return paises
        except (Exception) as error:
            messagebox.showerror(
                "Error",
                f"No se pudo leer el archivo JSON:\n{error}",
                parent=self.ventana,
            )
            return {}

    def mostrar_capital(self, evento=None):
        """Muestra la capital del país seleccionado."""
        pais = self.pais_seleccionado.get()
        capital = self.paises.get(pais)

        if capital:
            self.resultado.set(f"La capital de {pais} es {capital}.")
        else:
            self.resultado.set("Selecciona un país de la lista.")

    def limpiar(self):
        """Borra la selección y el resultado."""
        self.pais_seleccionado.set("")
        self.resultado.set("Aquí aparecerá la capital")

    def salir(self):
        """Cierra la aplicación."""
        self.ventana.destroy()

    def ejecutar(self):
        self.ventana.mainloop()


if __name__ == "__main__":
    AplicacionCapitales().ejecutar()
