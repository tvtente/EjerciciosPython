import unittest
from Ejercicio991Reflex.o03_panel_control import PanelControlState


class PanelControlTests(unittest.TestCase):
    def setUp(self):
        self.state=PanelControlState(_reflex_internal_init=True)

    def test_add_edit_filter_and_graphs(self):
        s=self.state
        s.nuevo_cliente()
        s.guardar_cliente({'nombre':'Persona de prueba','email':'prueba@example.com','genero':'Prefiero no indicar','ciudad':'Zaragoza'})
        self.assertEqual(s.total,7)
        self.assertFalse(s.dialogo_abierto)
        self.assertEqual(sum(p['value'] for p in s.users_for_graph),7)
        s.buscar('prueba@example')
        self.assertEqual(s.visibles,1)
        self.assertEqual(sum(p['value'] for p in s.ciudades_para_grafica),1)
        cliente=s.clientes_visibles[0]
        s.editar_cliente(cliente.id)
        s.guardar_cliente({'nombre':cliente.nombre,'email':cliente.email,'genero':'Mujer','ciudad':'Madrid'})
        self.assertEqual(s.total,7)
        self.assertEqual(s.clientes_visibles[0].ciudad,'Madrid')
        self.assertEqual(s.users_for_graph[0]['value'],1)

    def test_invalid_and_duplicate_preserve_dialog_and_records(self):
        s=self.state;s.nuevo_cliente()
        for email in ['invalido','LUCIA@EXAMPLE.COM']:
            s.guardar_cliente({'nombre':'Prueba','email':email,'genero':'Mujer','ciudad':'Madrid'})
            self.assertTrue(s.error)
            self.assertTrue(s.dialogo_abierto)
            self.assertEqual(s.total,6)

    def test_delete_requires_confirmation_and_updates_graph(self):
        s=self.state
        s.eliminar_cliente();self.assertEqual(s.total,6)
        s.pedir_borrado(1);s.cambiar_confirmacion(False)
        s.eliminar_cliente();self.assertEqual(s.total,6)
        s.pedir_borrado(1);s.eliminar_cliente()
        self.assertEqual(s.total,5)
        self.assertEqual(sum(p['value'] for p in s.users_for_graph),5)
        s.restaurar_ejemplos();self.assertEqual(s.total,6)

    def test_empty_filter_and_session_isolation(self):
        s=self.state;s.buscar('sin-coincidencias-123')
        self.assertEqual(s.clientes_visibles,[])
        self.assertEqual(sum(p['value'] for p in s.users_for_graph),0)
        other=PanelControlState(_reflex_internal_init=True)
        self.assertEqual(other.visibles,6)


if __name__=='__main__':unittest.main()
