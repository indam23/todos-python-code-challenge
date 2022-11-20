from datetime import datetime, timezone

import pytest

from entities import TodoEntry
from persistence.mapper.memory import MemoryTodoEntryMapper
from persistence.repository import TodoEntryRepository


_storage = {
    1: TodoEntry(id=1, summary="Lorem Ipsum", created_at=datetime.now(tz=timezone.utc))
}

@pytest.fixture
def mapper():
    return MemoryTodoEntryMapper(storage=_storage)

@pytest.fixture
def repository(mapper):
    return TodoEntryRepository(mapper=mapper)