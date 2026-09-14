import unittest

from ..domain.carrito import actualizar_cesta, total_cesta
from ..domain.catalogo import buscar_fruta


class CarritoTest(unittest.TestCase):
    def test_actualizar_y_totalizar_cesta(self):
        cesta = {}

        actualizar_cesta(cesta, "manzana", "Manzana", "🍎", 1.95, 2)
        actualizar_cesta(cesta, "manzana", "Manzana", "🍎", 1.95, -0.5)

        self.assertEqual(cesta["manzana"]["kg"], 1.5)
        self.assertEqual(cesta["manzana"]["total"], 2.92)
        self.assertEqual(total_cesta(cesta), 2.92)

    def test_eliminar_producto_al_restarlo_completo(self):
        cesta = {}
        actualizar_cesta(cesta, "kiwi", "Kiwi", "🥝", 3.20, 1)

        actualizar_cesta(cesta, "kiwi", "Kiwi", "🥝", 3.20, -1)

        self.assertNotIn("kiwi", cesta)
        self.assertEqual(total_cesta(cesta), 0)

    def test_buscar_fruta_ignora_mayusculas_y_acentos(self):
        self.assertEqual(buscar_fruta("MELOCOTÓN"), ["melocoton"])
        self.assertIn("manzana", buscar_fruta("man"))


if __name__ == "__main__":
    unittest.main()
