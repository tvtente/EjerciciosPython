"""Operaciones CRUD. Cada operación abre, confirma y cierra su propia sesión."""
from datetime import timezone
from zoneinfo import ZoneInfo
from dataclasses import dataclass
from math import isfinite
from sqlalchemy import update
from sqlmodel import Session, select
from .models import Todo
from .database import get_engine, init_database


@dataclass
class TodoView:
    id: int
    title: str
    description: str
    completed: bool
    created_at: str
    formatted_date: str
    estimated_hours: float


def as_view(todo: Todo) -> TodoView:
    created = todo.created_at
    if created.tzinfo is None:
        created = created.replace(tzinfo=timezone.utc)
    return TodoView(id=todo.id,title=todo.title,description=todo.description or '',
                    completed=todo.completed,created_at=created.isoformat(),
                    formatted_date=created.astimezone(ZoneInfo('Europe/Madrid')).strftime('%d/%m/%Y %H:%M'),
                    estimated_hours=todo.estimated_hours)


def validate_text(title: str, description: str) -> tuple[str,str | None]:
    title,description = title.strip(),description.strip()
    if not title:
        raise ValueError('El título no puede estar vacío.')
    if len(title)>160 or len(description)>3000:
        raise ValueError('Máximo 160 caracteres en el título y 3000 en la descripción.')
    return title,description or None


class TodoRepository:
    def __init__(self,engine=None):
        self.engine = engine if engine is not None else get_engine()

    def initialize(self):
        init_database(self.engine)

    def list_all(self) -> list[TodoView]:
        with Session(self.engine) as session:
            rows = session.exec(select(Todo).order_by(Todo.created_at.desc(),Todo.id.desc())).all()
            return [as_view(todo) for todo in rows]

    def create(self,title: str,description: str='',estimated_hours: str='') -> TodoView:
        title,description = validate_text(title,description)
        try:
            hours = float(estimated_hours.strip().replace(',','.') or '0')
        except ValueError:
            raise ValueError('Las horas estimadas deben ser un número válido.') from None
        if not isfinite(hours) or hours < 0:
            raise ValueError('Las horas estimadas deben ser un número finito mayor o igual que cero.')
        with Session(self.engine) as session:
            todo = Todo(title=title,description=description,estimated_hours=hours)
            session.add(todo)
            session.commit()
            session.refresh(todo)
            return as_view(todo)

    def edit(self,todo_id: int,title: str,description: str=''):
        title,description = validate_text(title,description)
        with Session(self.engine) as session:
            todo = session.get(Todo,todo_id)
            if todo is None:
                raise ValueError('La tarea ya no existe. Actualiza la lista.')
            todo.title,todo.description = title,description
            session.add(todo)
            session.commit()

    def set_completed(self,todo_id: int,completed: bool):
        with Session(self.engine) as session:
            result = session.exec(update(Todo).where(Todo.id==todo_id).values(completed=completed))
            if result.rowcount != 1:
                raise ValueError('La tarea ya no existe. Actualiza la lista.')
            session.commit()

    def delete(self,todo_id: int):
        with Session(self.engine) as session:
            todo = session.get(Todo,todo_id)
            if todo is None:
                raise ValueError('La tarea ya no existe. Actualiza la lista.')
            session.delete(todo)
            session.commit()
