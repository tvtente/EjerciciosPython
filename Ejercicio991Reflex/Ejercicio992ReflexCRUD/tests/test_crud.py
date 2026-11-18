"""Persistencia y CRUD sobre una base temporal: nunca usan data/todos.db."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main
from unittest.mock import patch
from sqlmodel import create_engine
from todo_app.models import Todo
from todo_app.repository import TodoRepository
from todo_app.todo_app import TodoState


class CrudTests(TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.url = f'sqlite:///{Path(self.directory.name)/"test.db"}'
        self.engine = create_engine(self.url,connect_args={'check_same_thread':False})
        self.repo = TodoRepository(self.engine)
        self.repo.initialize()

    def tearDown(self):
        self.engine.dispose()
        self.directory.cleanup()

    def test_full_crud_survives_new_connection(self):
        first = self.repo.create('  Grabar vídeo  ','  Preparar ejemplo  ')
        self.assertEqual(first.title,'Grabar vídeo')
        self.assertEqual(first.description,'Preparar ejemplo')
        self.repo.edit(first.id,'Grabar clase','')
        self.repo.set_completed(first.id,True)
        second_engine = create_engine(self.url)
        try:
            reopened = TodoRepository(second_engine).list_all()
            self.assertEqual(len(reopened),1)
            self.assertTrue(reopened[0].completed)
            self.assertEqual(reopened[0].created_at,first.created_at)
            self.assertEqual(reopened[0].title,'Grabar clase')
            self.assertEqual(reopened[0].description,'')
        finally:
            second_engine.dispose()
        self.repo.delete(first.id)
        self.assertEqual(self.repo.list_all(),[])
        next_task = self.repo.create('Otra tarea')
        self.assertGreater(next_task.id,first.id)

    def test_invalid_text_and_missing_id(self):
        for title,description in [('   ',''),('x'*161,''),('válido','x'*3001)]:
            with self.assertRaises(ValueError):self.repo.create(title,description)
        for action in [lambda:self.repo.edit(100,'válida'),lambda:self.repo.set_completed(100,True),lambda:self.repo.delete(100)]:
            with self.assertRaises(ValueError):action()
        self.assertEqual(self.repo.list_all(),[])

    def test_new_timestamp_per_instance(self):
        a,b=Todo(title='A'),Todo(title='B')
        self.assertIsNot(a.created_at,b.created_at)
        self.assertIsNotNone(a.created_at.tzinfo)

    def test_state_validation_edit_filters_and_database(self):
        s = TodoState(_reflex_internal_init=True)
        with patch('todo_app.todo_app.TodoRepository',lambda:self.repo):
            s.load_todos()
            s.set_new_title(' ');s.add_todo()
            self.assertTrue(s.error)
            s.set_new_title('Aprender Reflex');s.set_new_description('Practicar SQL');s.add_todo()
            self.assertFalse(s.error)
            self.assertEqual(s.new_title,'')
            task=s.todos[0]
            s.toggle_complete(task.id,True)
            self.assertEqual(s.completed_count,1)
            s.set_filter('Pendientes');self.assertEqual(s.visible_todos,[])
            s.set_filter('Todas');s.set_search('sql');self.assertEqual(len(s.visible_todos),1)
            s.start_edit(task.id);s.set_edit_title(' ');s.update_todo()
            self.assertTrue(s.edit_open);self.assertTrue(s.edit_error)
            s.set_edit_title('Reflex CRUD');s.update_todo()
            self.assertFalse(s.edit_open)
            self.assertEqual(s.todos[0].title,'Reflex CRUD')
            other = TodoState(_reflex_internal_init=True);other.load_todos()
            self.assertEqual(other.todos[0].title,'Reflex CRUD')
            s.ask_delete(task.id);s.delete_todo()
            self.assertEqual(self.repo.list_all(),[])


if __name__=='__main__':main()
