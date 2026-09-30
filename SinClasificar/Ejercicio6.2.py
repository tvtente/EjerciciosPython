import SinClasificar.Utilitario as Utilitario
import re


# Nombre: letras, espacios y acentos.
patron_nombre = r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+(?: [A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+)*$"
# Edad: números enteros desde 1 hasta 120.
patron_edad = r"^(?:[1-9]\d?|1[01]\d|120)$"
# Dirección: letras, números y símbolos habituales; entre 5 y 100 caracteres.
patron_direccion = r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9ºª.,#\-/ ]{5,100}$"
# Teléfono: entre 7 y 15 dígitos; puede comenzar por +.
patron_telefono = r"^\+?\d{7,15}$"

salir = ""

try:
    while salir != "s":
        Utilitario.borro()
        print("DATOS PERSONALES\n")

        nombre = input("¿Cómo te llamas? ").strip()
        while not re.fullmatch(patron_nombre, nombre):
            nombre = input("⚠️ Escribe un nombre válido: ").strip()

        edad = input("¿Cuántos años tienes? ").strip()
        while not re.fullmatch(patron_edad, edad):
            edad = input("⚠️ Escribe una edad entre 1 y 120: ").strip()

        direccion = input("¿Cuál es tu dirección? ").strip()
        while not re.fullmatch(patron_direccion, direccion):
            direccion = input("⚠️ Escribe una dirección válida: ").strip()

        telefono = input("¿Cuál es tu número de teléfono? ").replace(" ", "").replace("-", "")
        while not re.fullmatch(patron_telefono, telefono):
            telefono = input("⚠️ Escribe un teléfono válido: ").replace(" ", "").replace("-", "")

        persona = {"nombre": nombre, "edad": edad, "direccion": direccion, "telefono": telefono}

        print(f"\n{persona['nombre']} tiene {persona['edad']} años.")
        print(f"Vive en {persona['direccion']}.")
        print(f"Su teléfono es {persona['telefono']}.")

        salir = input("\nPulsa Enter para otra persona o S para salir: ").strip().lower()
        while salir not in ("", "s"):
            salir = input("⚠️ Pulsa Enter o escribe S para salir: ").strip().lower()

except KeyboardInterrupt:
    print("\n\n🛑 Programa cancelado con Ctrl+C.")

else:
    print("\n👋 Programa finalizado.")
