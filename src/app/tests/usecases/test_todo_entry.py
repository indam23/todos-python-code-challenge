from datetime import datetime, timezone

import pytest

from entities import TodoEntry
from usecases import (
    get_todo_entry,
    update_existing_todo_entry,
    create_todo_entry,
    UseCaseError,
    NotFoundError,
)

from tests.conftest import EXISTING_TODO_ID, NONEXISTENT_TODO_ID


@pytest.mark.asyncio
async def test_get_todo_entry(memory_repository) -> None:
    entity = await get_todo_entry(
        identifier=EXISTING_TODO_ID, repository=memory_repository
    )

    assert isinstance(entity, TodoEntry)


@pytest.mark.asyncio
async def test_get_not_existing_todo_entry(memory_repository) -> None:
    with pytest.raises(NotFoundError):
        await get_todo_entry(
            identifier=NONEXISTENT_TODO_ID, repository=memory_repository
        )


@pytest.mark.asyncio
async def test_create_todo_entry(memory_repository) -> None:
    data = TodoEntry(summary="Lorem ipsum", created_at=datetime.now(tz=timezone.utc))
    entity = await create_todo_entry(entity=data, repository=memory_repository)

    assert isinstance(entity, TodoEntry)


@pytest.mark.asyncio
async def test_todo_entry_creation_error(no_memory_repository) -> None:
    data = TodoEntry(summary="Lorem ipsum", created_at=datetime.now(tz=timezone.utc))
    with pytest.raises(UseCaseError):
        await create_todo_entry(entity=data, repository=no_memory_repository)


@pytest.mark.parametrize(
    "initial_entity, updated_entity",
    [
        (
            TodoEntry(summary="Lorem ipsum", created_at=datetime.now(tz=timezone.utc)),
            TodoEntry(summary="Lorem ipsum", created_at=datetime.now(tz=timezone.utc)),
        ),
        (
            TodoEntry(summary="Lorem ipsum", created_at=datetime.now(tz=timezone.utc)),
            TodoEntry(
                summary="Lorem ipsum",
                created_at=datetime.now(tz=timezone.utc),
                tags=["important"],
            ),
        ),
    ],
)
@pytest.mark.asyncio
async def test_update_existing_todo_entry(
    memory_repository, initial_entity, updated_entity
) -> None:
    entity = await create_todo_entry(
        entity=initial_entity, repository=memory_repository
    )

    actual_updated_entity = await update_existing_todo_entry(
        identifier=entity.id,
        updated_entity=updated_entity,
        repository=memory_repository,
    )
    assert actual_updated_entity == updated_entity


@pytest.mark.asyncio
async def test_update_not_existing_todo_entry(memory_repository) -> None:
    with pytest.raises(NotFoundError):
        data = TodoEntry(
            id=NONEXISTENT_TODO_ID,
            summary="Lorem ipsum",
            created_at=datetime.now(tz=timezone.utc),
        )
        await update_existing_todo_entry(
            identifier=NONEXISTENT_TODO_ID,
            updated_entity=data,
            repository=memory_repository,
        )
