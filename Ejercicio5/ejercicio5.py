import subprocess,platform
def limpiar_pantalla(): #Incorporarmos limpiar pantalla en una Funcion().
    if platform.system()=="Windows":subprocess.run(["cls"], shell=True) #shell es necesario en los subprocesos.
    else: subprocess.run(["clear"])

limpiar_pantalla()

while True:
    entrada = input("Introduce tus horas de trabajo (o escribe 'salir' para terminar): ")
    
    if entrada.lower() == "salir":
        print("\n¡Hasta luego!")
        input("\npresionar intro para borrar")
        limpiar_pantalla()
        break
    try:
        horas = float(entrada)
        coste = float(input("Introduce lo que cobras por hora €: "))
        paga = horas * coste
        
        # Formato europeo: puntos para miles y coma para decimales
        paga_formateada = f"{paga:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        print(f"Tu paga es {paga_formateada} €\n")
        input("Pulsa intro para nuevo calculo") #Retenemos proceso hasta pulsar Intro.
        limpiar_pantalla()
    except ValueError:
        limpiar_pantalla()
        print("Por favor, introduce un número válido o la palabra 'salir'.\n")