import subprocess, platform, time
import Ejercicio63RaimonConstantes as const


# ==========================================
# 2. DEFINICIÓN DE FUNCIONES AUXILIARES - UTILIDADES
# ==========================================

ES_WINDOWS      = platform.system() == "Windows"
COMANDO_LIMPIAR = ["cls"] if ES_WINDOWS else ["clear"]


def generar_cabecera():
    """Genera dinámicamente el menú visual de frutas en 3 columnas."""
    lineas = [
        "==================================================================================================================",
        f"                                    🛒 {const.BOLD}FRUTERÍA - PUNTO DE VENTA{const.RESET}                     ",
        "      Selecciona fruta, ajusta peso (+/-/*), cobra en efectivo o tarjeta y genera e imprime ticket      ",
        "==================================================================================================================",
        " ┌────────────────────┬──────────┬──┬────────────────────┬──────────┬──┬────────────────────┬──────────┐ ",
        " │ FRUTA              │ PVP / Kg │  │ FRUTA              │ PVP / Kg │  │ FRUTA              │ PVP / Kg │ ",
        " ├────────────────────┼──────────┼──┼────────────────────┼──────────┼──┼────────────────────┼──────────┤ "
    ]
    
    fila_actual = " "
    # Recorremos todas las frutas una a una
    for contador, (icono, nombre, precio) in enumerate(const.FRUTAS.values(), start=1):
        #Formateamos la cedal de la fruta actual
        precio_formateado = formato_precio(precio)
        celda = f"| {icono} {nombre:<15} | {precio_formateado:>8} |"
        
        #Añadimos a la fila actual
        # Unimos las celdas usando 2 espacios de separación entre cada una
        if fila_actual == " ":
            fila_actual += celda
        else:
            fila_actual += "  " + celda
        
        #cada 3 frutas, guardamos la fila y la reiniciamos
        if contador % 3 == 0:
            lineas.append(fila_actual)
            fila_actual= " "
            
    #Si al terminar el bucle queda alguna fruta suelta, la añadimos
    if fila_actual.strip():
        lineas.append(fila_actual)
            
    #Añadimos la parte inferior de la cabecera y los comandos
    lineas.append(" └────────────────────┴──────────┴──┴────────────────────┴──────────┴──┴────────────────────┴──────────┘ ")
    lineas.append(f" 🎮 COMANDOS: {const.AMARILLO}[/]{const.RESET} Nuevo pedido     {const.CYAN}[%]{const.RESET} Generar Ticket   {const.ROJO}[Ctrl+C]{const.RESET} Salir")
    lineas.append(f" ⚖️  Kg (EJ.): {const.VERDE}[+3,5]{const.RESET} Sumar         {const.VERDE}[-2,7]{const.RESET} Restar        {const.VERDE}[*1,9]{const.RESET} Fijar      (Límite: {const.BOLD}hasta 10 Kg{const.RESET})")
    lineas.append("==================================================================================================================")
    
    return "\n".join(lineas) + "\n"
    

# ┌──────────────────────────────────────────────────────────┐
# │ FUNCIÓN:     limpiar_pantalla()                          │
# │ DESCRIPCIÓN: Limpia la terminal y reimprime la cabecera  │
# └──────────────────────────────────────────────────────────┘
def limpiar_pantalla():
    subprocess.run(COMANDO_LIMPIAR, shell=ES_WINDOWS)
    print(generar_cabecera())
    
    
# ┌─────────────────────────────────────────────────────────────────────────────┐
# │ FUNCIÓN:     mostrar_mensaje()                                              │
# │ DESCRIPCIÓN: Notificación temporal con borrado dinámico                     │
# │ ENTRADA:     texto (str), tipo (str), segundos (int), lineas_a_borrar (int) │
# └─────────────────────────────────────────────────────────────────────────────┘
def mostrar_mensaje(texto, tipo="error", segundos=3, lineas_a_borrar=3):
    icono = const.BANDERAS.get(tipo, const.BANDERAS["warning"])
    print(f"\n{icono}  {texto}")
    time.sleep(segundos)
    #limpiar_buffer()
    
    secuencia_borrado = f"{const.SUBIR}{const.BORRAR}" * lineas_a_borrar
    print(secuencia_borrado, end="", flush=True)


# ┌──────────────────────────────────────────────────────────┐
# │ FUNCIÓN:     pedir_confirmacion()                        │
# │ DESCRIPCIÓN: Captura confirmación del usuario (s/n)      │
# │ ENTRADA:     mensaje (str), tipo (str)                   │
# │ SALIDA:      bool (True si 's'/'si', False en otro caso) │
# └──────────────────────────────────────────────────────────┘
def pedir_confirmacion(mensaje, tipo="pregunta"):
    icono = const.BANDERAS.get(tipo, const.BANDERAS["pregunta"])
    respuesta = input(f"\n{icono}  {mensaje} (s/n): ").strip().lower()
    return respuesta in ["s", "si"]


# ┌──────────────────────────────────────────────────────────┐
# │ FUNCIÓN:     formato_precio()                            │
# │ DESCRIPCIÓN: Formatea importes a string en euros (€)     │
# │ ENTRADA:     numero (float)                              │
# │ SALIDA:      str (ej: '4,50 €')                          │
# └──────────────────────────────────────────────────────────┘
def formato_precio(numero):
    return f"{numero:.2f} €".replace(".", ",")
