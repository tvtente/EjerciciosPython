import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def cambiar_tema():
    """Cambia al siguiente tema disponible."""
    temas = ["darkly", "solar", "superhero", "cosmo", "flatly", "litera"]
    tema_actual = app.style.theme.name
    indice_actual = temas.index(tema_actual) if tema_actual in temas else 0
    nuevo_tema = temas[(indice_actual + 1) % len(temas)]
    app.style.theme_use(nuevo_tema)
    etiqueta_tema.config(text=f"Tema actual: {nuevo_tema}")


def mostrar_mensaje():
    """Muestra en un diálogo el mensaje escrito en la entrada."""
    texto = entrada.get().strip()
    if not texto:
        texto = "¡Hola, TTKBootstrap!"

    dialogo = ttk.Toplevel(app)
    dialogo.title("Mensaje")
    dialogo.geometry("300x150")
    dialogo.transient(app)

    app.update_idletasks()
    x = app.winfo_x() + (app.winfo_width() - 300) // 2
    y = app.winfo_y() + (app.winfo_height() - 150) // 2
    dialogo.geometry(f"300x150+{x}+{y}")

    ttk.Label(
        dialogo,
        text=texto,
        font=("Helvetica", 12),
        wraplength=250,
    ).pack(expand=YES, fill=BOTH, padx=20, pady=20)

    ttk.Button(
        dialogo,
        text="Cerrar",
        bootstyle="danger",
        command=dialogo.destroy,
    ).pack(pady=10)

    dialogo.grab_set()


app = ttk.Window(themename="darkly")
app.title("Demo Básica de TTKBootstrap")
app.geometry("600x650")
app.resizable(True, True)

frame_principal = ttk.Frame(app, padding=20)
frame_principal.pack(fill=BOTH, expand=YES)

titulo = ttk.Label(
    frame_principal,
    text="Bienvenido a TTKBootstrap",
    font=("Helvetica", 24),
    bootstyle="inverse-primary",
)
titulo.pack(pady=20)

etiqueta_tema = ttk.Label(
    frame_principal,
    text="Tema actual: darkly",
    font=("Helvetica", 12),
)
etiqueta_tema.pack(pady=5)

boton_tema = ttk.Button(
    frame_principal,
    text="Cambiar Tema",
    bootstyle="info",
    command=cambiar_tema,
)
boton_tema.pack(pady=10)

ttk.Separator(frame_principal).pack(fill=X, pady=20)

frame_entrada = ttk.Frame(frame_principal)
frame_entrada.pack(fill=X, pady=10)

ttk.Label(
    frame_entrada,
    text="Escribe un mensaje:",
    font=("Helvetica", 12),
).pack(side=LEFT, padx=5)

entrada = ttk.Entry(frame_entrada, width=30)
entrada.pack(side=LEFT, padx=5, fill=X, expand=YES)

boton_mensaje = ttk.Button(
    frame_entrada,
    text="Mostrar",
    bootstyle="success",
    command=mostrar_mensaje,
)
boton_mensaje.pack(side=LEFT, padx=5)

frame_botones = ttk.Labelframe(
    frame_principal,
    text="Estilos de Botones",
    padding=10,
)
frame_botones.pack(fill=X, pady=20)

estilos = ["primary", "secondary", "success", "danger", "warning", "info"]
for estilo in estilos:
    ttk.Button(
        frame_botones,
        text=estilo.capitalize(),
        bootstyle=estilo,
    ).pack(side=LEFT, padx=5, pady=10)

frame_controles = ttk.Labelframe(
    frame_principal,
    text="Otros Controles",
    padding=10,
)
frame_controles.pack(fill=X, pady=10)

progreso = ttk.Progressbar(
    frame_controles,
    bootstyle="success-striped",
    value=75,
    maximum=100,
)
progreso.pack(fill=X, pady=10)

ttk.Scale(
    frame_controles,
    from_=0,
    to=100,
    value=75,
    command=lambda valor: progreso.configure(value=float(valor)),
).pack(fill=X, pady=10)

frame_checks = ttk.Frame(frame_controles)
frame_checks.pack(fill=X, pady=10)

for indice, texto in enumerate(["Opción 1", "Opción 2", "Opción 3"]):
    ttk.Checkbutton(
        frame_checks,
        text=texto,
        bootstyle=estilos[indice % len(estilos)],
    ).pack(side=LEFT, padx=10)

pie = ttk.Label(
    app,
    text="TTKBootstrap - Interfaces modernas para Python",
    bootstyle="inverse-secondary",
)
pie.pack(side=BOTTOM, fill=X, pady=5)

app.mainloop()