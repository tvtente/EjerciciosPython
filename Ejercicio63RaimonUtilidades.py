import subprocess, platform, time
import Ejercicio63RaimonConstantes as const


ES_WINDOWS      = platform.system() == "Windows"
COMANDO_LIMPIAR = ["cls"] if ES_WINDOWS else ["clear"]




# ┌──────────────────────────────────────────────────────────┐
# │ FUNCIÓN:     limpiar_pantalla()                          │
# │ DESCRIPCIÓN: Limpia la terminal y reimprime la cabecera  │
# └──────────────────────────────────────────────────────────┘
def limpiar_pantalla():
    subprocess.run(COMANDO_LIMPIAR, shell=ES_WINDOWS)
    print(const.CABECERA)
    
    
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


