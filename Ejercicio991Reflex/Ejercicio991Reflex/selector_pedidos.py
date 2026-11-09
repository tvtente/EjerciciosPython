"""Dispersión SVG con selección accesible: usa el canal habitual de eventos Reflex.

Complementa el ejemplo XY cuando su canal binario/renderizador no funciona.
"""
from pathlib import Path
from typing import Any
import reflex as rx


class OrderSelector(rx.Component):
    tag = 'OrderSelector'
    data: rx.Var[list[dict[str, Any]]]
    selected: rx.Var[list[str] | None]
    on_pick: rx.EventHandler[lambda ids: [ids]]

    def add_imports(self):
        return {'react': ['useState']}

    def add_custom_code(self):
        return [Path(__file__).with_name('selector_pedidos.jsx').read_text()]
