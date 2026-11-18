"""CRUD reconstruido: nombres y estructura reconocibles en las capturas del vídeo."""
import logging
import reflex as rx
from .repository import TodoRepository, TodoView

logger = logging.getLogger(__name__)


class TodoState(rx.State):
    todos: list[TodoView] = []
    new_title: str = ''
    new_description: str = ''
    new_estimated_hours: str = ''
    error: str = ''
    search: str = ''
    status_filter: str = 'Todas'
    editing_id: int = 0
    edit_title: str = ''
    edit_description: str = ''
    edit_open: bool = False
    edit_error: str = ''
    delete_id: int = 0
    delete_title: str = ''
    delete_open: bool = False

    @rx.var
    def visible_todos(self) -> list[TodoView]:
        text = self.search.strip().casefold()
        return [todo for todo in self.todos
                if (not text or text in f'{todo.title} {todo.description}'.casefold())
                and (self.status_filter=='Todas'
                     or (self.status_filter=='Completadas' and todo.completed)
                     or (self.status_filter=='Pendientes' and not todo.completed))]

    @rx.var
    def total(self) -> int:
        return len(self.todos)

    @rx.var
    def completed_count(self) -> int:
        return sum(todo.completed for todo in self.todos)

    @rx.event
    def set_new_title(self,value: str):
        self.new_title = value

    @rx.event
    def set_new_description(self,value: str):
        self.new_description = value

    @rx.event
    def set_new_estimated_hours(self,value: str):
        self.new_estimated_hours = value

    @rx.event
    def set_search(self,value: str):
        self.search = value

    @rx.event
    def set_filter(self,value: str):
        if value in ['Todas','Pendientes','Completadas']:
            self.status_filter = value

    def _report(self,exc,action: str) -> str:
        if isinstance(exc,ValueError):
            return str(exc)
        logger.exception('Error de base de datos al %s',action)
        return f'No se pudo {action}. Comprueba el archivo de base de datos y vuelve a intentarlo.'

    @rx.event
    def load_todos(self):
        """Leer la base real al entrar, actualizar o completar una operación."""
        try:
            repo = TodoRepository()
            repo.initialize()
            self.todos = repo.list_all()
            self.error = ''
        except Exception as exc:
            self.error = self._report(exc,'cargar las tareas')

    @rx.event
    def add_todo(self):
        try:
            TodoRepository().create(self.new_title,self.new_description,
                                    estimated_hours=self.new_estimated_hours)
        except Exception as exc:
            self.error = self._report(exc,'guardar la tarea')
            return
        self.new_title = ''
        self.new_description = ''
        self.new_estimated_hours = ''
        self.load_todos()
        return rx.toast.success('Tarea añadida correctamente')

    @rx.event
    def toggle_complete(self,todo_id: int,completed: bool):
        """Guardar el valor de la casilla, sin invertir una copia potencialmente antigua."""
        try:
            TodoRepository().set_completed(todo_id,completed)
            self.load_todos()
        except Exception as exc:
            self.error = self._report(exc,'actualizar la tarea')

    @rx.event
    def start_edit(self,todo_id: int):
        todo = next((todo for todo in self.todos if todo.id==todo_id),None)
        if todo:
            self.editing_id = todo.id
            self.edit_title,self.edit_description = todo.title,todo.description
            self.edit_error = ''
            self.edit_open = True

    @rx.event
    def set_edit_title(self,value: str):
        self.edit_title = value

    @rx.event
    def set_edit_description(self,value: str):
        self.edit_description = value

    @rx.event
    def set_edit_open(self,value: bool):
        self.edit_open = value

    @rx.event
    def update_todo(self):
        try:
            TodoRepository().edit(self.editing_id,self.edit_title,self.edit_description)
        except Exception as exc:
            self.edit_error = self._report(exc,'editar la tarea')
            return
        self.edit_open = False
        self.load_todos()
        return rx.toast.success('Tarea actualizada')

    @rx.event
    def ask_delete(self,todo_id: int):
        todo = next((todo for todo in self.todos if todo.id==todo_id),None)
        if todo:
            self.delete_id,self.delete_title = todo.id,todo.title
            self.delete_open = True

    @rx.event
    def set_delete_open(self,value: bool):
        self.delete_open = value

    @rx.event
    def delete_todo(self):
        try:
            TodoRepository().delete(self.delete_id)
        except Exception as exc:
            self.error = self._report(exc,'eliminar la tarea')
            return
        self.delete_open = False
        self.delete_id = 0
        self.load_todos()
        return rx.toast.info('Tarea eliminada')

def todo_item(todo: rx.Var[TodoView]):
    """Casilla, título tachado, descripción opcional, fecha y acciones."""
    return rx.box(rx.flex(
        rx.checkbox(checked=todo.completed,on_change=lambda checked:TodoState.toggle_complete(todo.id,checked),
                    aria_label='Completar tarea: '+todo.title,size='3'),
        rx.vstack(
            rx.text(todo.title,weight='bold',size='4',color='#f8fafc',
                    text_decoration=rx.cond(todo.completed,'line-through','none'),overflow_wrap='anywhere'),
            rx.text(rx.cond(todo.description!='',todo.description,'Sin descripción'),color='#cbd5e1',size='2',
                    white_space='pre-wrap',overflow_wrap='anywhere'),
            rx.text('Creado: ',todo.formatted_date,color='#94a3b8',size='1'),
            align='start',gap='8px',flex='1',min_width='0'),
        rx.flex(rx.button('Editar',on_click=TodoState.start_edit(todo.id),size='1',variant='soft'),
                rx.button('Eliminar',on_click=TodoState.ask_delete(todo.id),size='1',color_scheme='red',variant='soft'),
                gap='8px',flex_wrap='wrap'),align='start',gap='14px',flex_wrap='wrap'),
        padding='18px',background_color='#1e293b',border='1px solid #475569',border_radius='10px',width='100%')


def todo_form():
    return rx.form(rx.vstack(
        rx.input(placeholder='Título',name='title',aria_label='Título',required=True,max_length=160,
                 value=TodoState.new_title,on_change=TodoState.set_new_title,width='100%',size='3'),
        rx.text_area(placeholder='Descripción (opcional)',name='description',aria_label='Descripción',max_length=3000,
                     value=TodoState.new_description,on_change=TodoState.set_new_description,width='100%',min_height='100px'),
        rx.grid(
            # Espacio reservado para Fecha límite y Prioridad.
            rx.box(height='76px'),rx.box(height='76px'),
            rx.vstack(
                rx.hstack(rx.icon('clock',size=18),rx.text('Horas estimadas',weight='medium'),align='center',gap='8px'),
                rx.input(type='number',name='estimated_hours',aria_label='Horas estimadas',
                         placeholder='0',min=0,step=0.5,width='100%',size='3',
                         value=TodoState.new_estimated_hours,
                         on_change=TodoState.set_new_estimated_hours,
                         style={'& input':{'appearance':'auto','MozAppearance':'auto'},
                                '& input::-webkit-inner-spin-button':{'WebkitAppearance':'auto','opacity':'1'}}),
                align='start',gap='8px',width='100%',min_width='0'),
            # Espacios reservados para Recordatorio y Progreso.
            rx.box(),rx.box(height='64px',grid_column='1 / -1'),
            columns='2',gap='14px',width='100%'),
        rx.button('Añadir tarea',type='submit',width='100%',size='3'),
        gap='14px',width='100%'),on_submit=lambda _:TodoState.add_todo(),reset_on_submit=False,width='100%')


def todo_list():
    return rx.cond(TodoState.visible_todos.length()>0,
        rx.vstack(rx.foreach(TodoState.visible_todos,todo_item),gap='12px',width='100%'),
        rx.center(rx.vstack(rx.icon('clipboard-list',size=30,color='#93c5fd'),
            rx.text('No hay tareas en esta vista.',weight='bold'),
            rx.text('Añade una tarea o cambia los filtros.',size='2',color='#cbd5e1'),
            align='center',gap='10px'),padding='36px',border='1px dashed #475569',border_radius='10px',width='100%'))


def dialogs():
    return rx.fragment(
        rx.dialog.root(rx.dialog.content(
            rx.dialog.title('Editar tarea'),rx.dialog.description('Modifica el título y la descripción. La fecha y el estado se conservan.'),
            rx.form(rx.vstack(
                rx.input(value=TodoState.edit_title,on_change=TodoState.set_edit_title,required=True,max_length=160,aria_label='Título de la tarea'),
                rx.text_area(value=TodoState.edit_description,on_change=TodoState.set_edit_description,max_length=3000,aria_label='Descripción de la tarea'),
                rx.cond(TodoState.edit_error!='',rx.callout(TodoState.edit_error,color_scheme='red',role='alert')),
                rx.flex(rx.dialog.close(rx.button('Cancelar',variant='soft',type='button')),
                        rx.button('Guardar cambios',type='submit'),justify='end',gap='12px'),
                align='stretch',gap='16px',margin_top='18px'),on_submit=lambda _:TodoState.update_todo(),reset_on_submit=False)),
            open=TodoState.edit_open,on_open_change=TodoState.set_edit_open),
        rx.alert_dialog.root(rx.alert_dialog.content(
            rx.alert_dialog.title('¿Eliminar la tarea?'),rx.alert_dialog.description(TodoState.delete_title),
            rx.text('Esta operación elimina el registro de la base de datos.',size='2',margin_top='12px'),
            rx.flex(rx.alert_dialog.cancel(rx.button('Cancelar',variant='soft')),
                    rx.alert_dialog.action(rx.button('Sí, eliminar',on_click=TodoState.delete_todo,color_scheme='red')),
                    justify='end',gap='12px',margin_top='20px')),
            open=TodoState.delete_open,on_open_change=TodoState.set_delete_open))


def index():
    """Composición visible en frame_00321: encabezado → formulario → lista."""
    return rx.box(rx.vstack(
        rx.flex(rx.box(rx.badge('EJERCICIO 992 · CRUD + SQLITE',color_scheme='blue'),
                       rx.heading('Lista de tareas',size='8',margin_top='12px'),
                       rx.text('Crea, edita y completa tus tareas. Se conservan al reiniciar.',color='#cbd5e1',margin_top='10px')),
                rx.button(rx.icon('refresh-cw',size=16),'Actualizar',variant='soft',on_click=TodoState.load_todos),
                justify='between',flex_wrap='wrap',gap='16px',width='100%'),
        rx.separator(size='4'),todo_form(),
        rx.cond(TodoState.error!='',rx.callout(TodoState.error,color_scheme='red',role='alert')),
        rx.flex(rx.badge(TodoState.total,' tareas'),rx.badge(TodoState.completed_count,' completadas',color_scheme='green'),
                gap='10px',width='100%'),
        rx.flex(rx.input(placeholder='Buscar título o descripción…',aria_label='Buscar tareas',value=TodoState.search,
                          on_change=TodoState.set_search,flex='1',min_width='180px'),
                rx.select(['Todas','Pendientes','Completadas'],value=TodoState.status_filter,on_change=TodoState.set_filter,
                          aria_label='Filtrar por estado'),gap='12px',flex_wrap='wrap',width='100%'),
        todo_list(),
        rx.text('SQLite persistente · Hora local de Madrid · Pulsa Actualizar para ver cambios de otras sesiones.',size='1',color='#94a3b8'),
        dialogs(),align='stretch',gap='22px',max_width='760px',margin='0 auto'),
        background_color='#0f172a',color='#f8fafc',min_height='100vh',padding=['20px','40px'])


app = rx.App()
app.add_page(index,title='Lista de tareas · CRUD Reflex',on_load=TodoState.load_todos)
