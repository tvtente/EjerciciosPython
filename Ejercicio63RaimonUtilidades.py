import subprocess, platform
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