import platform
def limpiar_pantalla(): #Incorporarmos limpiar pantalla en una Funcion().
    if platform.system()=="Windows":subprocess.run(["cls"], shell=True) #shell es necesario en los subprocesos.
    else: subprocess.run(["clear"])

import subprocess

limpiar_pantalla()