from typing import List

from sqlalchemy import Column, DateTime, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import functions

from entities import TodoEntry
from persistence.db.base import Base
from persistence.db.models.tags import Tag

todo_tag_association_table = Table(
    "todo_tag_association_table",
    Base.metadata,
    Column("todo_id", ForeignKey("todos.id")),
    Column("tag_id", ForeignKey("tags.id")),
)


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    summary = Column(String, nullable=False)
    detail = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=functions.now())
    tags = relationship(
        "Tag", secondary=todo_tag_association_table, backref="todos", lazy="joined"
    )

    def __init__(
        self, summary: str, detail: str = None, tags: List[Tag] = None, **kwargs
    ):
        self.summary = summary
        self.detail = detail
        if not tags:
            self.tags = list()
        else:
            self.tags = tags

    def as_dict(self):
        return {
            "id": self.id,
            "summary": self.summary,
            "detail": self.detail,
            "created_at": self.created_at,
            "tags": [tag.tag for tag in self.tags],
        }

    def as_entry(self):
        data = self.as_dict()
        entity = TodoEntry(**data)
        return entity
