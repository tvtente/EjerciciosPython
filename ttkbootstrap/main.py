#!/usr/bin/python3
"""
titulo Principal

Descripcion principal

UI source file: eventos_pack.ui
"""
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu
from mainui import ControlEventosUI

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "eventos_pack.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class ControlEventos(ControlEventosUI):
    def __init__(self, master=None):
        super().__init__(
            master,
            project_ui=PROJECT_UI,
            resource_paths=RESOURCE_PATHS,
            translator=None,
            on_first_object_cb=None
        )
        self.builder.connect_callbacks(self)


if __name__ == "__main__":
    root = tk.Tk()
    app = ControlEventos(root)
    app.run()
