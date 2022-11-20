from datetime import datetime, timezone

import pytest

from entities import TodoEntry
from persistence.mapper.memory import MemoryTodoEntryMapper
from persistence.repository import TodoEntryRepository
from usecases import get_todo_entry, update_existing_todo_entry, create_todo_entry, UseCaseError, NotFoundError

@pytest.mark.asyncio
async def test_get_todo_entry(repository) -> None:
    entity = await get_todo_entry(identifier=1, repository=repository)

    assert isinstance(entity, TodoEntry)


@pytest.mark.asyncio
async def test_get_not_existing_todo_entry(repository) -> None:
    with pytest.raises(NotFoundError):
        await get_todo_entry(identifier=42, repository=repository)


@pytest.mark.asyncio
async def test_create_todo_entry(repository) -> None:
    data = TodoEntry(summary="Lorem ipsum", created_at=datetime.now(tz=timezone.utc))
    entity = await create_todo_entry(entity=data, repository=repository)

    assert isinstance(entity, TodoEntry)


@pytest.mark.asyncio
async def test_todo_entry_creation_error() -> None:
    mapper = MemoryTodoEntryMapper(storage=None)
    repository = TodoEntryRepository(mapper=mapper)

    data = TodoEntry(summary="Lorem ipsum", created_at=datetime.now(tz=timezone.utc))
    with pytest.raises(UseCaseError):
        await create_todo_entry(entity=data, repository=repository)


@pytest.mark.parametrize(
    "initial_entity, updated_entity",
    [
        (
            TodoEntry(summary="Lorem ipsum", created_at=datetime.now(tz=timezone.utc)),
            TodoEntry(summary="Lorem ipsum", created_at=datetime.now(tz=timezone.utc)),
        ),
        (
            TodoEntry(summary="Lorem ipsum", created_at=datetime.now(tz=timezone.utc)),
            TodoEntry(summary="Lorem ipsum", created_at=datetime.now(tz=timezone.utc), tags=["important"]),
        ),
        (
            TodoEntry(summary="Lorem ipsum", created_at=datetime.now(tz=timezone.utc), tags=["important"]),
            TodoEntry(summary="Lorem ipsum", created_at=datetime.now(tz=timezone.utc)),
        ),
        (
            TodoEntry(summary="Lorem ipsum", created_at=datetime.now(tz=timezone.utc)),
            TodoEntry(summary="Lorem ipsum", created_at=datetime.now(tz=timezone.utc), detail="some detail"),
        ),
    ]
    
)
@pytest.mark.asyncio
async def test_update_existing_todo_entry(repository, initial_entity, updated_entity) -> None:
    entity = await create_todo_entry(entity=initial_entity, repository=repository)

    id = entity.id
    actual_updated_entity = await update_existing_todo_entry(identifier=id, updated_entity=updated_entity, repository=repository)
    assert actual_updated_entity == updated_entity


@pytest.mark.asyncio
async def test_get_not_existing_todo_entry(repository) -> None:
    with pytest.raises(NotFoundError):
        data = TodoEntry(summary="Lorem ipsum", created_at=datetime.now(tz=timezone.utc))
        await update_existing_todo_entry(identifier=42, updated_entity=data, repository=repository)
