#!/usr/bin/python3
"""
hola

hola mundo

UI source file: saludar.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import principalui as baseui


class principal(baseui.principalUI):
    def __init__(self, master=None):
        super().__init__(master)

    def registrar_asistente(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = principal(root)
    app.run()
