
# ==========================================
# 1. CONSTANTES DEL SISTEMA
# ==========================================

from .Ejercicio63RaimonBDD import FRUTAS


BOLD            = "\033[1m"
ROJO            = "\033[31;1m"
VERDE           = "\033[32m"
NARANJA         = "\033[38;5;208m"
AMARILLO        = "\033[93m"
CYAN            = "\033[96m"
RESET           = "\033[0m"

SUBIR           = "\033[1A" 
BORRAR          = "\033[2K" 

TIPO_IVA        = 0.04

ERROR = f"{ROJO}❌ERROR{RESET}"
PREGUNTA = f"{CYAN}❓PREGUNTA{RESET}"

ICONO_PREGUNTA = "❓"


BANDERAS = {
    "error": "❌",
    "warning": "⚠️",
    "info": "ℹ️",
    "exito": "✅",
    "pregunta": "❓",
}


