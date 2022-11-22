from persistence.db.models.todos import Todo
from entities import TodoEntry

from tests.conftest import (
    EXISTING_TODO_ID,
    EXISTING_TODO_DATA,
    NEW_TODO_ID,
    NEW_TODO_DATA,
)

def test_get_todo(sql_mapper, session, existing_todo):
    todo = sql_mapper.get_todo(identifier=EXISTING_TODO_ID, session=session)
    assert isinstance(todo, Todo)
    assert todo.id == EXISTING_TODO_ID
    assert todo.summary == EXISTING_TODO_DATA["summary"]


def test_create_todo(sql_mapper, session, existing_todo):
    data = {k:v for k,v in NEW_TODO_DATA.items() if k != "id"}
    todo_entry = TodoEntry(**data)
    todo = sql_mapper.create_todo(entity=todo_entry, session=session)
    assert isinstance(todo, Todo)
    assert todo.id == NEW_TODO_ID
    assert todo.summary == NEW_TODO_DATA["summary"]


def test_update_todo(sql_mapper, session, existing_todo):
    todo_entry = TodoEntry(**EXISTING_TODO_DATA)
    tag_text = "important"
    todo_entry.tags = [tag_text]
    todo = sql_mapper.update_todo(identifier=EXISTING_TODO_ID, updated_entity=todo_entry, session=session)
    assert isinstance(todo, Todo)
    assert todo.id == EXISTING_TODO_ID
    assert todo.summary == EXISTING_TODO_DATA["summary"]
    assert len(todo.tags) == 1
    assert todo.tags[0].tag == tag_text
