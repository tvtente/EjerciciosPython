class Motocicleta:
    # Atributo de clase
    estado = "nuevo"

    # Presionar F2 para cambiar el nombre en todas las partes del script.

    # Método
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
        # ATRIBUTOS DE INSTANCIA
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

    def arrancar(self):  # Mejorar los dos prints
        if self.motor_arrancado:
            print(
                "Se detiene el motor. Se escucha un molesto sonido al girar "
                "la llave. El motor ya estaba arrancado."
            )
        else:
            self.motor_arrancado = True
            print("Se ha arrancado el motor. Bruuuuhm!!!")

    def detener(self):  # Mejorar los dos prints
        if self.motor_arrancado:  # modifico el if por if not
            self.motor_arrancado = False
            print("Se detiene el motor.")
        else:
            print("No puede parar el motor, porque ya está apagado.")

    def consultar_precio(self):
        print(
            f"El precio de la motocicleta {self.marca} {self.modelo} "
            f"es de {self.precio} €."
        )

    def comprobar_deposito(self):
        print(f"=== REPORTE DE DÉPOSITO DE {self.marca} {self.modelo} ===")
        print(f"El deposito tiene {self.combustible_litros} litros.")
        print(
            "La capacidad máxima del tanque de combustible es de "
            f"{self.combustible_maximo}."
        )
        print(
            f"Faltan {self.combustible_maximo - self.combustible_litros} "
            "litros para llenar el del depósito"
        )
        print("=== FIN DEL REPORTE ===\n")

    def repostar(self):
        while True:
            self.repostar_litros = float(
                input("Por favor, introduzca la cantidad de litros que desea repostar:\n")
            )

            if self.combustible_litros + self.repostar_litros <= self.combustible_maximo:
                print("Repostaje exitoso.")
                print(f"Se han repostado {self.repostar_litros} litros")
                self.combustible_litros += self.repostar_litros
                print(f"El depósito tiene {self.combustible_litros} litros de combustible")
                break

            print("No cabe tanto combustible.")


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

motocicleta_yamaha_1.arrancar()
motocicleta_yamaha_1.arrancar()

motocicleta_yamaha_1.detener()
motocicleta_yamaha_1.detener()

motocicleta_yamaha_1.comprobar_deposito()

motocicleta_yamaha_1.repostar()

# print(f"El precio de la motocicleta{motocicleta_harley_1.marca} {motocicleta_harley_1.modelo} es de {motocicleta_harley_1.precio} €.")
