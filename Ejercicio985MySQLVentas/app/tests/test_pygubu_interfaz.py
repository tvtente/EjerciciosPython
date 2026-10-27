"""Pruebas de eventos reales de la interfaz, siempre con datos en memoria."""
import os
from pathlib import Path
import sys
import time
import unittest
from unittest.mock import patch

APP_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_DIR))
import app
from app_pygubu import ClientesPygubuApp
from clientes_datos import ClientesDemo


@unittest.skipUnless(os.getenv("DISPLAY") or sys.platform in ("win32", "darwin"), "Requiere un escritorio gráfico")
class InterfazPygubuTest(unittest.TestCase):
    def setUp(self):
        self.info = patch.object(app.messagebox, "showinfo").start()
        self.error = patch.object(app.messagebox, "showerror").start()
        self.confirmar = patch.object(app.messagebox, "askyesno", return_value=True).start()
        self.addCleanup(patch.stopall)
        self.ventana = ClientesPygubuApp(demo=True)
        self.ventana.update()
        self.ventana.withdraw()
        self.addCleanup(self._cerrar)

    def _cerrar(self):
        self.ventana.cerrar()

    def esperar(self):
        limite = time.monotonic() + 5
        # Completar también los refrescos asíncronos que dispara guardar.
        while self.ventana.ocupado or not self.ventana.eventos.empty():
            self.ventana.update()
            if time.monotonic() > limite:
                self.fail("La interfaz no terminó su operación")
            time.sleep(0.01)
        self.ventana.update()

    def seleccionar(self, cliente_id):
        self.ventana.tabla.selection_set(str(cliente_id))
        self.ventana.update()  # Dispara <<TreeviewSelect>> definido en el .ui.
        self.assertEqual(self.ventana.seleccionado, cliente_id)

    def test_botones_crud_y_seleccion_del_xml(self):
        w = self.ventana
        self.assertIsNone(w.builder.connect_callbacks(w))
        self.assertEqual(len(w.tabla.get_children()), 3)
        w.campos["Nombre"].set("Elena")
        w.campos["Apellido1"].set("D'Ávila")
        w.campos["Categoria"].set("0")
        w.guardar_btn.invoke()  # command="guardar" en el XML.
        self.esperar()
        self.assertEqual(len(w.tabla.get_children()), 4)
        self.seleccionar(4)
        self.assertEqual(w.campos["Categoria"].get(), "0")
        w.campos["Ciudad"].set("Córdoba")
        w.guardar_btn.invoke()
        self.esperar()
        self.assertEqual(w.repositorio.filas[4]["Ciudad"], "Córdoba")
        w.busqueda.set("4")
        w.buscar_btn.invoke()
        self.esperar()
        self.assertEqual(len(w.tabla.get_children()), 1)
        self.seleccionar(4)
        w.eliminar_btn.invoke()
        self.esperar()
        self.assertNotIn(4, w.repositorio.filas)
        w.todos_btn.invoke()
        self.esperar()
        self.assertEqual(len(w.tabla.get_children()), 3)
        self.error.assert_not_called()

    def test_enter_busca_y_limpieza(self):
        w = self.ventana
        # Los eventos de teclado requieren una ventana visible con foco.
        w.deiconify()
        w.update()
        w.entrada_busqueda.focus_force()
        w.update()
        w.busqueda.set("Ana")
        w.entrada_busqueda.event_generate("<Return>")
        self.esperar()
        self.assertEqual(list(w.filas), [3])
        self.seleccionar(3)
        w.nuevo_btn.invoke()
        self.assertIsNone(w.seleccionado)
        self.assertEqual(w.campos["Nombre"].get(), "")
        w.guardar_btn.invoke()
        self.error.assert_called_once()

    def test_conectar_llama_al_repositorio(self):
        w = self.ventana
        w.demo = False
        w._botones()
        repo = ClientesDemo()
        # El botón ejecuta conectar(), sin usar servidores ni credenciales reales.
        with patch.object(app, "ClientesMySQL", return_value=repo) as factory:
            w.conectar_btn.invoke()
            self.esperar()
        factory.assert_called_once()
        self.assertIs(w.repositorio, repo)
        self.assertEqual(len(w.tabla.get_children()), 3)
        self.error.assert_not_called()


if __name__ == "__main__":
    unittest.main()
