"""Pruebas del contrato de selección XY; ejecutar desde Ejercicio991Reflex."""
import unittest
from unittest.mock import patch, Mock
from Ejercicio991Reflex.o10_graficos_vinculados import LinkedChartsState, selection_ids, RECORDS


def event(rows=None, count=2, **changes):
    selection={'kind':'box','mode':'replace','cleared':False,'truncated':False,
               'total_count':count,'rows':rows if rows is not None else [{'trace':0,'index':0},{'trace':0,'index':1}]}
    selection.update(changes)
    return {'type':'select_end','version':1,'token':'test','selection':selection}


class LinkedChartsTests(unittest.TestCase):
    def test_selection_filters_table_and_totals(self):
        state=LinkedChartsState(_reflex_internal_init=True)
        state.select_points(event())
        self.assertEqual([r['id'] for r in state.visible_rows],['pedido-a','pedido-b'])
        self.assertEqual(state.total_revenue,'300.00 €')
        state.select_points(event([{'trace':0,'index':4}],count=1))
        self.assertEqual([r['id'] for r in state.visible_rows],['pedido-e'])

    def test_empty_is_not_clear(self):
        state=LinkedChartsState(_reflex_internal_init=True)
        state.select_points(event([],count=0))
        self.assertEqual(state.selected_ids,[])
        self.assertEqual(state.visible_rows,[])
        state.select_points(event([],count=0,kind='clear',cleared=True))
        self.assertIsNone(state.selected_ids)
        self.assertEqual(len(state.visible_rows),len(RECORDS))

    def test_invalid_event_preserves_previous_filter(self):
        state=LinkedChartsState(_reflex_internal_init=True)
        state.try_first_two()
        for rows in [[{'trace':1,'index':0}],[{'trace':0,'index':999}],
                     [{'trace':0,'index':True}],[{'trace':0,'index':-1}]]:
            state.select_points(event(rows,count=1))
            self.assertTrue(state.error)
            self.assertEqual(state.selected_ids,['pedido-a','pedido-b'])

    def test_truncated_selection_uses_resolver(self):
        resolved=Mock()
        resolved.rows.return_value=[{'trace':0,'index':0},{'trace':0,'index':1}]
        with patch('Ejercicio991Reflex.o10_graficos_vinculados.rxy.resolve_selection',return_value=resolved) as resolver:
            self.assertEqual(selection_ids(event([{'trace':0,'index':0}],truncated=True)),['pedido-a','pedido-b'])
            resolver.assert_called_once()
        with patch('Ejercicio991Reflex.o10_graficos_vinculados.rxy.resolve_selection',return_value=None):
            with self.assertRaises(ValueError):selection_ids(event(truncated=True))

    def test_reset_remounts_source_chart(self):
        state=LinkedChartsState(_reflex_internal_init=True)
        state.try_first_two()
        old=state.generation
        state.reset_selection()
        self.assertIsNone(state.selected_ids)
        self.assertGreater(state.generation,old)
        self.assertFalse(state.error)


if __name__=='__main__':unittest.main()
