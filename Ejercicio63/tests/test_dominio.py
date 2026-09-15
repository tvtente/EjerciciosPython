import unittest

from dominio.carrito import agregar, eliminar, peso_total, subtotal
from dominio.reglas import calcular_bolsas, calcular_envio, calcular_total_final


class DominioTest(unittest.TestCase):
    def setUp(self):
        self.producto = {
            "codigo": "02",
            "tipo": "peso",
            "cantidad": 2.0,
            "peso": 2.0,
            "precio": 0.8,
            "unidad": "kg.",
            "subtotal": 1.6,
        }

    def test_agregar_producto_y_calcular_totales(self):
        carrito = {}

        agregar(carrito, "🍎 Manzana", self.producto)

        self.assertEqual(subtotal(carrito), 1.6)
        self.assertEqual(peso_total(carrito), 2.0)
        self.assertEqual(carrito["🍎 Manzana"]["cantidad"], 2.0)

    def test_agregar_acumula_productos_del_mismo_nombre(self):
        carrito = {}

        agregar(carrito, "🍎 Manzana", self.producto)
        agregar(carrito, "🍎 Manzana", {**self.producto, "cantidad": 1.0, "peso": 1.0, "subtotal": 0.8})

        self.assertEqual(carrito["🍎 Manzana"]["cantidad"], 3.0)
        self.assertEqual(carrito["🍎 Manzana"]["peso"], 3.0)
        self.assertEqual(subtotal(carrito), 2.4)

    def test_eliminar_devuelve_el_producto(self):
        carrito = {"🍎 Manzana": self.producto}

        eliminado = eliminar(carrito, "🍎 Manzana")

        self.assertEqual(eliminado, self.producto)
        self.assertEqual(carrito, {})

    def test_envio_y_bolsas(self):
        self.assertEqual(calcular_bolsas(0), 0)
        self.assertEqual(calcular_bolsas(5.1), 2)
        self.assertEqual(calcular_envio("1", "2"), 4.5)
        self.assertEqual(calcular_envio("1", "1"), 0.0)

    def test_total_final_no_muta_el_carrito(self):
        carrito = {"🍎 Manzana": self.producto}

        total = calcular_total_final(carrito, "1", "2")

        self.assertEqual(total, 6.1)
        self.assertNotIn("👜 Bolsa", carrito)


if __name__ == "__main__":
    unittest.main()
