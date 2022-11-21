from typing import List

from sqlalchemy.orm import Session

from entities import TodoEntry
from persistence.mapper.errors import (
    EntityNotFoundMapperError,
    CreateMapperError,
    UpdateMapperError,
)
from persistence.mapper.interfaces import TodoEntryMapperInterface
from persistence.db.db_access import DbAccessLayer
from persistence.db.models.todos import Todo
from persistence.db.models.tags import Tag


class SqlTodoEntryMapper(TodoEntryMapperInterface):
    def __init__(self, db: DbAccessLayer) -> None:
        self.db = db

    async def get(self, identifier: int) -> TodoEntry:
        with self.db.session() as session:
            todo = self.get_todo(identifier=identifier, session=session)
            return todo.as_entry()


    def get_todo(self, identifier: int, session: Session) -> TodoEntry:
        try:
            todo = session.query(Todo).filter(Todo.id == identifier).first()
            if not todo:
                raise EntityNotFoundMapperError
            return todo
        except EntityNotFoundMapperError:
            raise EntityNotFoundMapperError(
                f"Entity `id:{identifier}` was not found."
            )

    async def create(self, entity: TodoEntry) -> TodoEntry:
        with self.db.session() as session:
            todo = self.create_todo(entity=entity, session=session)
            return todo.as_entry()

    def create_todo(self, entity: TodoEntry, session: Session) -> TodoEntry:
        try:
            entity.tags = self.create_tags(entity.tags, session)
            todo = Todo(**entity.dict())
            session.add(todo)
            session.commit()
            return todo
        except Exception as e:
            raise UpdateMapperError(e)

    def create_tags(self, tag_texts: List[str], session: Session) -> TodoEntry:
        tags = []
        for tag_text in tag_texts:
            tag = self.create_tag(tag_text, session)
            tags.append(tag)
        return tags

    def create_tag(self, tag_text: str, session: Session) -> TodoEntry:
        try:
            tag = session.query(Tag).filter(Tag.tag == tag_text).first()
            if not tag:
                tag = Tag(tag_text)
            return tag
        except:
            raise CreateMapperError()

    async def update(self, identifier: int, updated_entity: TodoEntry) -> TodoEntry:
        with self.db.session() as session:
            updated_todo = self.update_todo(
                identifier=identifier, updated_entity=updated_entity, session=session
            )
            return updated_todo.as_entry()

    def update_todo(
        self, identifier: int, updated_entity: TodoEntry, session: Session
    ) -> TodoEntry:
        try:
            todo = self.get_todo(identifier=identifier, session=session)
            updated_tags = self.create_tags(updated_entity.tags, session)
            updated_entity.tags = updated_tags
            for key, val in updated_entity.dict().items():
                setattr(todo, key, val)
            session.commit()
            return todo
        except EntityNotFoundMapperError:
            raise EntityNotFoundMapperError(f"Entity `id:{identifier}` was not found.")
        except Exception as e:
            raise UpdateMapperError(e)
