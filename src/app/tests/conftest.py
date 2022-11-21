from datetime import datetime, timezone

import pytest

from entities import TodoEntry
from persistence.mapper.memory import MemoryTodoEntryMapper
from persistence.repository import TodoEntryRepository


EXISTING_TODO_ID = 1
NONEXISTENT_TODO_ID = 42
EXISTING_TODO_DATA = {
    "id": EXISTING_TODO_ID,
    "summary": "Lorem Ipsum",
    "created_at": datetime.now(tz=timezone.utc),
}

_memory_storage = {EXISTING_TODO_ID: TodoEntry(**EXISTING_TODO_DATA)}


@pytest.fixture
def memory_mapper():
    return MemoryTodoEntryMapper(storage=_memory_storage)


@pytest.fixture
def memory_repository(memory_mapper):
    return TodoEntryRepository(mapper=memory_mapper)


@pytest.fixture
def no_memory_mapper():
    return MemoryTodoEntryMapper(storage=None)


@pytest.fixture
def no_memory_repository(no_memory_mapper):
    return TodoEntryRepository(mapper=no_memory_mapper)
