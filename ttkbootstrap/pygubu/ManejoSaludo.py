#!/usr/bin/python3
"""
hola

hola mundo

UI source file: saludar.ui
"""
import tkinter as tk
import tkinter.ttk as ttk


def safe_i18n_translator(value):
    """i18n - Setup translator in derived class file"""
    return value


def safe_fo_callback(widget):
    """on first objec callback - Setup callback in derived class file."""
    pass


def safe_image_loader(master, image_name: str):
    """Image loader - Setup image_loader in derived class file."""
    return tk.PhotoImage(file=image_name, master=master)


def find_callback(callbacks_bag, callback_uid):
    cb = None

    if isinstance(callbacks_bag, dict):
        if callback_uid in callbacks_bag:
            cb = callbacks_bag[callback_uid]
    elif hasattr(callbacks_bag, callback_uid):
        cb = getattr(callbacks_bag, callback_uid)
    if cb is None:

        def cb_undef(*args):
            print(f"No function defined for {callback_uid}")

        cb = cb_undef
    return cb


def saludo(
    master=None,
    *,
    translator=None,
    on_first_object_cb=None,
    data_pool=None,
    image_loader=None,
    callbacks_bag=None,
):
    if translator is None:
        translator = safe_i18n_translator
    _ = translator  # i18n string marker.
    if image_loader is None:
        image_loader = safe_image_loader
    if on_first_object_cb is None:
        on_first_object_cb = safe_fo_callback

    #
    # Begin UI code
    frame1 = ttk.Frame(master)
    frame1.configure(height=750, width=750)
    # First object created
    on_first_object_cb(frame1)

    lblNombre = ttk.Label(frame1, name="lblnombre")
    lblNombre.configure(text='Nombre')
    lblNombre.pack(side="top")
    entNombre = ttk.Entry(frame1, name="entnombre")
    entNombre.pack(side="top")
    btnSaludar = ttk.Button(frame1, name="btnsaludar")
    btnSaludar.configure(text='Saludar')
    btnSaludar.pack(side="top")
    btnSaludar.configure(
        command=find_callback(
            callbacks_bag,
            "registrar_asistente"))
    frame1.pack(side="top")

    return frame1


if __name__ == "__main__":
    root = tk.Tk()
    app = saludo(root)
    if isinstance(app, tk.Menu):
        root.configure(menu=app)
    root.mainloop()
