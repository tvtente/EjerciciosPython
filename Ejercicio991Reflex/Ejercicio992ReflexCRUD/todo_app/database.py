"""Engine propio: SQLite local por defecto, sin modificar la configuración de otros ejercicios."""
from functools import lru_cache
from pathlib import Path
import os
from sqlmodel import SQLModel, create_engine

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
    # Crea tablas faltantes sin borrar datos; no sustituye migraciones de esquemas existentes.
    from .models import Todo  # registrar metadatos antes de create_all
    SQLModel.metadata.create_all(engine if engine is not None else get_engine())
