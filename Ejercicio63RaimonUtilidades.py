import subprocess, platform, time
import Ejercicio63RaimonConstantes as const

ES_WINDOWS      = platform.system() == "Windows"
COMANDO_LIMPIAR = ["cls"] if ES_WINDOWS else ["clear"]

CABECERA        = (
    "================================================================================================\n"
    f"                                 🛒 {const.BOLD}FRUTERÍA - PUNTO DE VENTA{const.RESET}                     \n"
    f"  Selecciona fruta, ajusta peso (+/-/*), cobra en efectivo o tarjeta y genera e imprime ticket      \n"
    "================================================================================================\n"
    " ┌─────────────────┬──────────┬──┬─────────────────┬──────────┬──┬─────────────────┬──────────┐ \n"
    " │ FRUTA           │ PVP / Kg │  │ FRUTA           │ PVP / Kg │  │ FRUTA           │ PVP / Kg │ \n"
    " ├─────────────────┼──────────┼──┼─────────────────┼──────────┼──┼─────────────────┼──────────┤ \n"
    " │ 🍒 Cereza       │  4,50 €  │  │ 🥭 Mango        │  3,50 €  │  │ 🍐 Pera         │  2,15 €  │ \n"
    " │ 🌴 Dátil        │  6,20 €  │  │ 🍎 Manzana      │  1,95 €  │  │ 🍍 Piña         │  1,80 €  │ \n"
    " │ 🍓 Fresa        │  3,80 €  │  │ 🍑 Melocotón    │  2,40 €  │  │ 🍌 Plátano      │  2,10 €  │ \n"
    " │ 🥝 Kiwi         │  3,20 €  │  │ 🍈 Melón        │  1,20 €  │  │ 🍉 Sandía       │  0,95 €  │ \n"
    " │ 🍋 Limón        │  1,60 €  │  │ 🍊 Naranja      │  1,50 €  │  │ 🍇 Uva          │  2,90 €  │ \n"
    " └─────────────────┴──────────┴──┴─────────────────┴──────────┴──┴─────────────────┴──────────┘ \n"
    f" 🎮 COMANDOS: {const.AMARILLO}[/]{const.RESET} Nuevo pedido     {const.CYAN}[%]{const.RESET} Generar Ticket   {const.ROJO}[Ctrl+C]{const.RESET} Salir\n"
    f" ⚖️  Kg (EJ.): {const.VERDE}[+3,5]{const.RESET} Sumar         {const.VERDE}[-2,7]{const.RESET} Restar        {const.VERDE}[*1,9]{const.RESET} Fijar      (Límite: {const.BOLD}hasta 10 Kg{const.RESET})\n"
    "================================================================================================\n"
)


# ┌──────────────────────────────────────────────────────────┐
# │ FUNCIÓN:     limpiar_pantalla()                          │
# │ DESCRIPCIÓN: Limpia la terminal y reimprime la cabecera  │
# └──────────────────────────────────────────────────────────┘
def limpiar_pantalla():
    subprocess.run(COMANDO_LIMPIAR, shell=ES_WINDOWS)
    print(CABECERA)
    
    
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


