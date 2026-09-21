class Motocicleta:
    """Representa una motocicleta y las acciones básicas que puede realizar."""

    # Atributo de clase
    estado = "nuevo"

    def __init__(
        self,
        color,
        matricula,
        combustible_litros,
        numero_ruedas,
        marca,
        modelo,
        fecha_fabricacion,
        velocidad_punta,
        peso,
        combustible_maximo,
    ):
        """Crea una motocicleta con sus atributos de instancia."""
        self.color = color
        self.matricula = matricula
        self.combustible_litros = combustible_litros
        self.numero_ruedas = numero_ruedas
        self.marca = marca
        self.modelo = modelo
        self.fecha_fabricacion = fecha_fabricacion
        self.velocidad_punta = velocidad_punta
        self.peso = peso
        self.combustible_maximo = combustible_maximo
        self.motor_arrancado = False

    def arrancar(self):
        """Arranca el motor si todavía está apagado."""
        if self.motor_arrancado:
            print(
                "El motor ya estaba arrancado. Se escucha un molesto sonido "
                "al girar la llave."
            )
        else:
            self.motor_arrancado = True
            print("Se ha arrancado el motor. Bruuuuhm!!!")

    def detener(self):
        """Detiene el motor si está encendido."""
        if self.motor_arrancado:
            self.motor_arrancado = False
            print("Se detiene el motor.")
        else:
            print("No puede parar el motor, porque ya está apagado.")

    def consultar_precio(self):
        """Muestra el precio asignado a la motocicleta."""
        print(f"El precio de la motocicleta {self.marca} {self.modelo} es de {self.precio} €.")

    def comprobar_deposito(self):
        """Muestra la cantidad actual y máxima de combustible."""
        print(f"=== REPORTE DE DÉPOSITO DE {self.marca} {self.modelo} ===")
        print(f"El deposito tiene {self.combustible_litros} litros.")
        print(
            "La capacidad máxima del tanque de combustible es de "
            f"{self.combustible_maximo}."
        )
        print(
            f"Faltan {self.combustible_maximo - self.combustible_litros} "
            "litros para llenar el depósito."
        )
        print("=== FIN DEL REPORTE ===\n")

    def repostar(self, cantidad_combustible):
        """Añade la cantidad indicada con el motor apagado y sin superar el máximo."""
        if self.motor_arrancado:
            print("No se puede repostar con el motor encendido.")
            return

        if cantidad_combustible <= 0:
            print("La cantidad debe ser mayor que cero.")
        elif self.combustible_litros + cantidad_combustible > self.combustible_maximo:
            print("No cabe tanto combustible.")
        else:
            self.combustible_litros += cantidad_combustible
            print("Repostaje exitoso.")
            print(f"Se han repostado {cantidad_combustible} litros.")
            print(f"El depósito tiene {self.combustible_litros} litros de combustible.")

    def consumir_combustible(self, litros):
        """Resta combustible si el depósito tiene la cantidad solicitada."""
        if litros <= 0:
            print("El consumo debe ser mayor que cero.")
        elif litros > self.combustible_litros:
            print("No hay suficiente combustible.")
        else:
            self.combustible_litros -= litros
            print(f"Combustible restante: {self.combustible_litros} litros.")

    def mostrar_ficha(self):
        """Muestra los datos principales de la motocicleta."""
        print(f"{self.marca} {self.modelo}")
        print(f"Matrícula: {self.matricula}")
        print(f"Precio: {self.precio} €")
        print(f"Combustible: {self.combustible_litros}/{self.combustible_maximo} L")


# INSTANCIAS de la clase Motocicleta
motocicleta_yamaha_1 = Motocicleta(
    "Azul y blanco",
    "4345 IHF",
    10,
    2,
    "Yamaha",
    "YZF-R",
    "20/02/2020",
    288,
    199,
    17,
)

motocicleta_harley_1 = Motocicleta(
    matricula="4324-HGER",
    combustible_litros=0,
    color="Negra",
    marca="Harley Davidson",
    modelo="Fat Boy",
    numero_ruedas=2,
    peso=304,
    fecha_fabricacion="29/09/2020",
    velocidad_punta=160,
    combustible_maximo=20,
)

motocicleta_harley_1.precio = 27000
motocicleta_yamaha_1.precio = 6000

motocicleta_harley_1.consultar_precio()
motocicleta_yamaha_1.consultar_precio()

motocicleta_yamaha_1.comprobar_deposito()
motocicleta_yamaha_1.arrancar()
motocicleta_yamaha_1.arrancar()
motocicleta_yamaha_1.repostar(3)
motocicleta_yamaha_1.consumir_combustible(5)
motocicleta_yamaha_1.detener()
motocicleta_yamaha_1.detener()
motocicleta_yamaha_1.repostar(3)
motocicleta_yamaha_1.comprobar_deposito()
motocicleta_yamaha_1.mostrar_ficha()
