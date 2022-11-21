from random import randint
from datetime import datetime, timezone

from entities import TodoEntry
from persistence.mapper.errors import (
    EntityNotFoundMapperError,
    CreateMapperError,
    UpdateMapperError,
)
from persistence.mapper.interfaces import TodoEntryMapperInterface


class MemoryTodoEntryMapper(TodoEntryMapperInterface):
    _storage: dict

    def __init__(self, storage: dict) -> None:
        self._storage = storage

    async def get(self, identifier: int) -> TodoEntry:
        try:
            return self._storage[identifier]
        except KeyError:
            raise EntityNotFoundMapperError(f"Entity `id:{identifier}` was not found.")

    async def create(self, entity: TodoEntry) -> TodoEntry:
        try:
            entity.id = self._generate_unique_id()
            entity.created_at = datetime.now(tz=timezone.utc)
            self._storage[entity.id] = entity
            return entity
        except TypeError as error:
            raise CreateMapperError(error)

    async def update(self, identifier: int, updated_entity: TodoEntry) -> TodoEntry:
        try:
            self._storage[identifier]
        except KeyError:
            raise EntityNotFoundMapperError(f"Entity `id:{identifier}` was not found.")
        try:
            updated_entity.updated_at = datetime.now(tz=timezone.utc)
            self._storage[identifier] = updated_entity
            return updated_entity
        except TypeError as error:
            raise UpdateMapperError(error)

    def _generate_unique_id(self) -> int:
        identifier = randint(1, 10_000)
        while identifier in self._storage:
            identifier = randint(1, 10_000)

        return identifier
