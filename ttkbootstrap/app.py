import ttkbootstrap as ttk
from ttkbootstrap.constants import *

app = ttk.Window(themename="darkly")
app.title("Ejemplo de TTKBootstrap")
app.geometry("400x300")

titulo = ttk.Label(app, text="Bienvenido a TTKBootstrap", font=("Helvetica", 16))
titulo.pack(pady=20)

boton_primario = ttk.Button(app, text="Botón Primario", bootstyle="primary")
boton_primario.pack(pady=10)    

boton_secundario = ttk.Button(app, text="Botón Secundario", bootstyle="secondary")
boton_secundario.pack(pady=10)

entrada = ttk.Entry(app, bootstyle="info")
entrada.pack(pady=10, padx=20, fill=X) 

app.mainloop()