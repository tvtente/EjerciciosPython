class Persona:
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido

    def nombre_completo(self):
        print(f"{self.nombre} {self.apellido}")


class Estudiante(Persona):
    def __init__(self, nombre, apellido, carrera):
        super().__init__(nombre, apellido)
        self.carrera = carrera

    def mostrar_carrera(self):
        print(self.carrera)
