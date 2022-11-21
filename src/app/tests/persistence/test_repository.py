from datetime import datetime, timezone

import pytest

from entities import TodoEntry
from persistence.errors import EntityNotFoundError, CreateError

from tests.conftest import EXISTING_TODO_ID, NONEXISTENT_TODO_ID, EXISTING_TODO_DATA


@pytest.mark.asyncio
async def test_get_todo_entry(memory_repository) -> None:
    entity = await memory_repository.get(identifier=EXISTING_TODO_ID)
    assert isinstance(entity, TodoEntry)


@pytest.mark.asyncio
async def test_todo_entry_not_found_error(memory_repository) -> None:
    with pytest.raises(EntityNotFoundError):
        await memory_repository.get(identifier=NONEXISTENT_TODO_ID)


@pytest.mark.asyncio
async def test_save_todo_entry(memory_repository) -> None:
    data = TodoEntry(
        summary="Buy flowers to my wife",
        detail="We have marriage anniversary"
    )

    entity = await memory_repository.create(entity=data)
    assert isinstance(entity, TodoEntry)
    assert entity.id > 1


@pytest.mark.asyncio
async def test_todo_entry_create_error(no_memory_repository) -> None:
    data = TodoEntry(
        summary="Lorem Ipsum",
        detail=None,
        created_at=datetime.now(tz=timezone.utc),
    )

    with pytest.raises(CreateError):
        await no_memory_repository.create(entity=data)


@pytest.mark.asyncio
async def test_update_todo_entry(memory_repository) -> None:
    data = TodoEntry(tags=["important"], **EXISTING_TODO_DATA)

    entity = await memory_repository.update(EXISTING_TODO_ID, updated_entity=data)
    assert isinstance(entity, TodoEntry)
    assert entity.id == EXISTING_TODO_ID


@pytest.mark.asyncio
async def test_update_todo_nonexistent_entry(memory_repository) -> None:
    data = TodoEntry(
        summary="Lorem Ipsum",
        detail=None,
        created_at=datetime.now(tz=timezone.utc),
    )

    with pytest.raises(EntityNotFoundError):
        await memory_repository.update(NONEXISTENT_TODO_ID, updated_entity=data)
