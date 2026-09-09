import unittest
from unittest.mock import patch

from .. import Ejercicio63RaimonCRUD as crud


class ComandosTest(unittest.TestCase):
    def test_porcentaje_requiere_confirmacion_con_cesta(self):
        cesta = {"manzana": {"total": 2.0}}

        with patch.object(crud.util, "pedir_confirmacion", return_value=True):
            resultado = crud.procesar_comando_global("%", cesta)

        self.assertEqual(resultado, "TICKET")

    def test_porcentaje_no_permite_ticket_con_cesta_vacia(self):
        with patch.object(crud.util, "mostrar_mensaje"):
            resultado = crud.procesar_comando_global("%", {})

        self.assertEqual(resultado, "CONTINUAR")

    def test_barra_cancela_la_cesta_con_confirmacion(self):
        cesta = {"manzana": {"total": 2.0}}

        with patch.object(crud.util, "pedir_confirmacion", return_value=True):
            with patch.object(crud.util, "mostrar_mensaje"):
                resultado = crud.procesar_comando_global("/", cesta)

        self.assertEqual(resultado, "CANCELAR")
        self.assertEqual(cesta, {})


if __name__ == "__main__":
    unittest.main()
