"""Engine propio: SQLite local por defecto, sin modificar la configuración de otros ejercicios."""
from functools import lru_cache
from pathlib import Path
import os
from sqlmodel import SQLModel, create_engine
from sqlalchemy import text

PROJECT = Path(__file__).resolve().parents[1]


@lru_cache(maxsize=1)
def get_engine():
    url = os.environ.get('TODO_DATABASE_URL')
    if not url:
        path = PROJECT / 'data' / 'todos.db'
        path.parent.mkdir(parents=True,exist_ok=True)
        url = f'sqlite:///{path}'
    options = {'check_same_thread':False, 'timeout':10} if url.startswith('sqlite:') else {}
    return create_engine(url,connect_args=options)


def init_database(engine=None):
    from .models import Todo  # registrar metadatos antes de create_all
    db_engine = engine if engine is not None else get_engine()

    # Para bases nuevas, crea las tablas con los campos del modelo.
    SQLModel.metadata.create_all(db_engine)

    # Esta actualización de tablas existentes es específica de SQLite.
    if db_engine.dialect.name != 'sqlite':
        return

    with db_engine.begin() as connection:
        columns = connection.execute(
            text('PRAGMA table_info(todos)')
        ).mappings().all()
        column_names = {column['name'] for column in columns}

        if 'estimated_hours' not in column_names:
            connection.execute(text(
                'ALTER TABLE todos '
                'ADD COLUMN estimated_hours REAL NOT NULL DEFAULT 0'
            ))