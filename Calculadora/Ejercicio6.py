import platform
import subprocess


def Borro():
    if platform.system() == "Windows":
        subprocess.run(["cls"], shell=True)
    else:
        subprocess.run(["clear"])


# Limpiar la consola al principio
Borro()


class Marino:

    def hablar(self):
        print("Hola soy un animal marino!")


class Pulpo(Marino):

    def hablar(self):
        print("Hola soy un pulpo!")


class Foca(Marino):

    def __init__(self, mensaje):
        self.mensaje = mensaje  # Atributo nuevo

    def hablar(self):
        print(self.mensaje)  # Muestra el atributo


# Pruebas
marino = Marino()
marino.hablar()

pulpo = Pulpo()
pulpo.hablar()

foca = Foca("Hola soy una foca!")
foca.hablar()