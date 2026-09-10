from pathlib import Path
import time
import pandas as pd

import platform
import subprocess


def limpiar_pantalla():
    """Limpia la consola según el sistema operativo."""
    comando = ["cls"] if platform.system() == "Windows" else ["clear"]
    subprocess.run(comando, shell=platform.system() == "Windows")
    
ruta_json = Path(__file__).with_name("titanic.json")
columnas = (
    ("PassengerId", "Id", 4),
    ("Survived", "Vive", 4),
    ("Pclass", "Clase", 8),
    ("Name", "Nombre", 26),
    ("Sex", "Sexo", 8),
    ("Age", "Edad", 4),
)

limpiar_pantalla()
with open(ruta_json, encoding="utf-8") as archivo:
    df = pd.read_json(archivo)[[nombre for nombre, titulo, ancho in columnas]]

while True:
    entrada = input("¿Cuántas filas deseas añadir? ").strip()
    if entrada.isdigit() and int(entrada) >= 0:
        n = int(entrada)
        break
    print("Introduce un número entero mayor que cero.")

siguiente_id = int(pd.to_numeric(df["PassengerId"]).max()) + 1 if not df.empty else 1

for numero in range(1, n + 1):
    fila = {"PassengerId": siguiente_id}
    print(f"\n--- Pasajero {numero} de {n} | PassengerId: {siguiente_id} ---")

    for columna in df.columns:
        if columna == "PassengerId":
            continue

        while True:
            valor = input(f"{columna}: ").strip()

            if valor == "":
                fila[columna] = pd.NA
                break

            try:
                if columna in ("Survived", "Pclass"):
                    fila[columna] = int(valor)
                elif columna == "Age":
                    fila[columna] = float(valor.replace(",", "."))
                else:
                    fila[columna] = valor
                break
            except ValueError:
                print(
                    "Introduce un valor numérico válido o pulsa Enter para dejarlo vacío."
                )

    df = pd.concat([df, pd.DataFrame([fila])], ignore_index=True)
    siguiente_id += 1

with open(ruta_json, "w", encoding="utf-8") as archivo:
    df.to_json(archivo, orient="records", indent=4, force_ascii=False)

print(f"\n✅ Se han añadido {n} filas a {ruta_json.name}.")
print("\n📄 Contenido de titanic.json:\n")
print("    " + " | ".join(f"{titulo:<{ancho}}" for nombre, titulo, ancho in columnas))
print(
    "─"
    * (4 + sum(ancho for nombre, titulo, ancho in columnas) + 3 * (len(columnas) - 1))
)

for indice, datos in df.iterrows():
    valores = []
    for (columna, titulo, ancho), valor in zip(columnas, datos.values):
        valor_mostrado = "Sin dato" if pd.isna(valor) else valor
        valores.append(f"{str(valor_mostrado):<{ancho}}")
    print(f"{indice + 1:02d}. " + " | ".join(valores))
    time.sleep(1)
