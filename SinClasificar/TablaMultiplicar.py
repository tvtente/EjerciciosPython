import platform
import subprocess
import time

def Borro():
    """Limpia la consola según el sistema operativo."""
    if platform.system() == "Windows":
        subprocess.run(["cls"], shell=True)
    else:
        subprocess.run(["clear"])


# Enter repite el programa; solo S permite salir.
salir = ""

while salir != "s":
    Borro()

    while True:
        try:
            entrada = input("Introduce un número entero positivo: ").strip()
            if 0 <= (numero := int(entrada)) < 10:
                raise ValueError
        except ValueError:
            print("⚠️ Debes escribir un número entero mayor que cero hsta 10.")
        else:
            break
        finally:
            print()

    print(f"\nTabla de multiplicar del {numero}:")
    print("-" * 20)

    for i in range(1, 11):
        print(f"{numero} x {i:2} = {(numero * i):3}")

    print("-" * 20)
    salir = input("\nPulsa Enter para otra tabla o S para salir: ").strip().lower()
    while salir not in ("", "s"):
        salir = input("⚠️ Pulsa Enter o escribe S para salir: ").strip().lower()

print("\n👋 Programa finalizado.")
time.sleep(3)
