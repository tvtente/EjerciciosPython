#!/usr/bin/python3
"""
titulo del pack

descripción de pack

UI source file: eventos_pack.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import controleventos_uiui as baseui


class ControlEventosPack(baseui.ControlEventosPackUI):
    def __init__(self, master=None):
        super().__init__(master)


if __name__ == "__main__":
    root = tk.Tk()
    app = ControlEventosPack(root)
    app.run()
