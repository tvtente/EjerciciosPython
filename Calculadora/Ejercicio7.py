import platform, subprocess, sys

# Limpia la consola
subprocess.run(["cls"] if (is_win := platform.system() == "Windows") else ["clear"], shell=is_win)


class Universidad:
    """Clase base que gestiona la información de la universidad."""
    
    def set_universidad(self, nombre_universidad):
        # Asigna el nombre de la universidad como atributo de instancia
        self.nombre_universidad = nombre_universidad
    
    def saludar(self):
        # Devuelve el mensaje de bienvenida propio de la Universidad
        return f"Bienvenidos a la Universidad de {self.nombre_universidad}"


class Carrera:
    """Clase base que gestiona la información de la carrera o especialidad."""
    
    def set_carrera(self, especialidad):
        # Asigna el nombre de la especialidad como atributo de instancia
        self.especialidad = especialidad
        
    def saludar(self):
        # Devuelve el mensaje de bienvenida propio de la Carrera
        return f"Bienvenidos a la carrera de {self.especialidad}"


# Herencia múltiple: Estudiante hereda tanto de Universidad como de Carrera.
# NOTA MRO (Method Resolution Order): Dado que ambas clases padre definen el método 'saludar',
# Python buscará primero en Universidad por ser la primera en la lista de herencia.
class Estudiante(Universidad, Carrera):

    def set_estudiante(self, nombre, edad):
        # Asigna los datos personales del estudiante
        self.nombre = nombre
        self.edad = edad

    def mostrar_datos(self):
        # Imprime un resumen utilizando atributos heredados y propios
        return(
            f"El estudiante es {self.nombre}, tiene {self.edad} años y cursa "
            f"{self.especialidad} en la Universidad de {self.nombre_universidad}."
        )


# --- Bloque de ejecución ---

# 1. Instanciación del objeto
persona = Estudiante()

# 2. Configuración de datos a través de los setters de las distintas clases
persona.set_universidad("Harvard")             # Método heredado de Universidad
persona.set_carrera("Ingeniería Electrónica")  # Método heredado de Carrera
persona.set_estudiante("Mike", 19)             # Método propio de Estudiante

# 3. Demostración del orden de resolución de métodos (MRO):
# Ejecuta Universidad.saludar() porque Universidad está declarada primero en Estudiante(Universidad, Carrera)
print("\n----- Saludo inicial ------")
print(persona.saludar())

# 4. Impresión de la información consolidada
print("\n--- Datos de la persona ---")
print(persona.mostrar_datos())
print()

sys.exit(0)