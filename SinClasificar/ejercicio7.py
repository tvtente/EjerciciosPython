import platform
import re
import subprocess


def borro():
    """Limpia la consola en Windows, Linux y macOS."""
    if platform.system() == "Windows":
        subprocess.run(["cls"], shell=True)
    else:
        subprocess.run(["clear"])


# Expresión regular para peso: admite de 1 a 500 kg.
# ^ y $ obligan a validar toda la entrada; [,.] permite coma o punto decimal.
# El caso 500 solo admite ceros decimales, para no aceptar valores mayores.
patron_peso = r"^(?:(?:[1-9]\d?|[1-4]\d{2})(?:[,.]\d+)?|500(?:[,.]0+)?)$"

# Expresión regular para estatura: admite de 0,5 a 2,5 m.
# Solo permite decimales dentro de ese intervalo.
patron_estatura = r"^(?:0[,.][5-9]\d*|1(?:[,.]\d+)?|2(?:[,.](?:[0-4]\d*|5(?:0*)?))?)$"

# Una cadena vacía inicia el primer cálculo.
opcion = ""

# El programa continúa hasta que el usuario escriba S.
while opcion != "s":
    borro()
    print("🧮 CÁLCULO DEL ÍNDICE DE MASA CORPORAL 🧮")
    print("ℹ️  Puedes usar punto (.) o coma (,) para los decimales.\n")

    try:
        peso_texto = input("¿Cuál es tu peso en kg? ⚖️ ").strip()
        while not re.fullmatch(patron_peso, peso_texto):
            print("⚠️  Peso no válido. Escribe un valor entre 1 y 500 kg; por ejemplo: 72,5.")
            peso_texto = input("🔁 Vuelve a escribir tu peso en kg: ").strip()

        estatura_texto = input("¿Cuál es tu estatura en metros? 📏 ").strip()
        while not re.fullmatch(patron_estatura, estatura_texto):
            print("⚠️  Estatura no válida. Escribe un valor entre 0,5 y 2,5 m; por ejemplo: 1,75.")
            estatura_texto = input("🔁 Vuelve a escribir tu estatura en metros: ").strip()

        # float() necesita punto decimal, por eso se cambia la coma.
        peso = float(peso_texto.replace(",", "."))
        estatura = float(estatura_texto.replace(",", "."))
        imc = round(peso / estatura ** 2, 2)

        # :.2f muestra siempre dos decimales.
        print(f"\n✅ Tu índice de masa corporal es 📝 {imc:.2f}")
    except ValueError:
        print("\n❌ Error: introduce números positivos usando punto o coma decimal.")
    except ZeroDivisionError:
        print("\n❌ Error: la estatura no puede ser 0.")
    except KeyboardInterrupt:
        print("\n🛑 Programa cancelado por el usuario.")
    except EOFError:
        print("\n❌ Error: no se recibió ningún dato.")

    print()
    # Enter repite el cálculo; solo S permite salir.
    opcion = input("🔁 Presione Enter para otro cálculo o S para salir: ").strip().lower()
    while opcion not in ("", "s"):
        opcion = input("⚠️ Opción no válida. Presione Enter o escriba S para salir: ").strip().lower()

print("👋 ¡Gracias por usar la calculadora de IMC!")
