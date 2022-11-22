from datetime import datetime, timezone
from entities import TodoEntry
from persistence.mapper.sql import SqlTodoEntryMapper
from persistence.mapper.memory import MemoryTodoEntryMapper
from persistence.db.db_access import DbAccessLayer, get_postgres_db_engine_from_env

EXISTING_TODO_ID = 1
EXISTING_TODO_DATA = {
    "id": EXISTING_TODO_ID,
    "summary": "Lorem Ipsum",
    "created_at": datetime.now(tz=timezone.utc),
}

_memory_storage = {EXISTING_TODO_ID: TodoEntry(**EXISTING_TODO_DATA)}


def init_mapper():
    try:
        db = DbAccessLayer(get_postgres_db_engine_from_env())
        mapper = SqlTodoEntryMapper(db)
    except:
        mapper = MemoryTodoEntryMapper(storage=_memory_storage)

    return mapper
