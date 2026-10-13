"""Ejercicio de herencia con una clase padre y dos clases hijas.

Moto hereda directamente el constructor de Fabrica. Carro define su propio
constructor porque necesita el atributo adicional numero_puertas y utiliza
super() para inicializar los atributos heredados.
"""
import platform, subprocess, sys

# Limpia la consola
subprocess.run(["cls"] if (is_win := platform.system() == "Windows") else ["clear"], shell=is_win)

class Fabrica:
    """Representa los datos comunes de los vehículos fabricados."""

    def __init__(self, llantas, color, precio):
        """Inicializa los datos y comprueba que llantas sea un entero."""

        llantas = str(llantas).strip()

        while not llantas.isdigit():
            llantas = input("Ingrese un valor entero para llantas: ").strip()

        self._llantas = int(llantas)
        self._color = color
        self._precio = precio


class Moto(Fabrica):
    """Representa una moto que hereda los atributos de Fabrica."""

    def cantidad(self):
        """Devuelve los datos de la moto como una cadena de texto.

        return no muestra el texto directamente. El valor devuelto se puede
        guardar, modificar o mostrar posteriormente mediante print().
        """

        return (
            "La cantidad de llantas: {}\nEl color es: {}\nEl precio es: {}".format(
                self._llantas,
                self._color,
                self._precio,
            )
        )


class Carro(Fabrica):
    """Representa un carro con un número de puertas propio."""

    def __init__(self, llantas, color, precio, numero_puertas):
        """Inicializa los atributos heredados y el atributo propio del carro.

        super() llama al constructor de Fabrica para no repetir la asignación
        de llantas, color y precio.
        """

        super().__init__(llantas, color, precio)
        self._numero_puertas = numero_puertas

    def cantidad(self):
        """Muestra directamente en pantalla todos los datos del carro.

        A diferencia de Moto.cantidad(), este método usa print() internamente
        y, por tanto, devuelve None de manera implícita.
        """

        print(
            "La cantidad de llantas: {}\n"
            "El color es: {}\n"
            "El precio es: {}\n"
            "El número de puertas es: {}".format(
                self._llantas,
                self._color,
                self._precio,
                self._numero_puertas,
            )
        )


print("OBJETO = moto")
moto = Moto("bonitas", "Gris", "$200")
print(moto.cantidad())

print()

print("OBJETO = carro")
carro = Carro(4, "Negro", "$600", 5)
carro.cantidad()

sys.exit(0)
