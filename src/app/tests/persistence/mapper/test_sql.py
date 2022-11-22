import pytest

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

@pytest.mark.asyncio
async def test_get(sql_mapper, existing_todo):
    todo_entry = await sql_mapper.get(identifier=EXISTING_TODO_ID)
    assert isinstance(todo_entry, TodoEntry)
    assert todo_entry.id == EXISTING_TODO_ID
    assert todo_entry.summary == EXISTING_TODO_DATA["summary"]

def test_create_todo(sql_mapper, session, existing_todo, new_todo_entry):
    todo = sql_mapper.create_todo(entity=new_todo_entry, session=session)
    assert isinstance(todo, Todo)
    assert todo.id == NEW_TODO_ID
    assert todo.summary == NEW_TODO_DATA["summary"]

@pytest.mark.asyncio
async def test_create(sql_mapper, existing_todo, new_todo_entry): 
    todo_entry = await sql_mapper.create(entity=new_todo_entry)
    assert isinstance(todo_entry, TodoEntry)
    assert todo_entry.id == NEW_TODO_ID
    assert todo_entry.summary == NEW_TODO_DATA["summary"]

def test_update_todo(sql_mapper, session, existing_todo, existing_todo_entry):
    tag_text = "important"
    existing_todo_entry.tags = [tag_text]
    todo = sql_mapper.update_todo(identifier=EXISTING_TODO_ID, updated_entity=existing_todo_entry, session=session)
    assert isinstance(todo, Todo)
    assert todo.id == EXISTING_TODO_ID
    assert todo.summary == EXISTING_TODO_DATA["summary"]
    assert len(todo.tags) == 1
    assert todo.tags[0].tag == tag_text

@pytest.mark.asyncio
async def test_update(sql_mapper, existing_todo, existing_todo_entry):
    tag_text = "important"
    existing_todo_entry.tags = [tag_text]
    todo_entry = await sql_mapper.update(identifier=EXISTING_TODO_ID, updated_entity=existing_todo_entry)
    assert isinstance(todo_entry, TodoEntry)
    assert todo_entry.id == EXISTING_TODO_ID
    assert todo_entry.summary == EXISTING_TODO_DATA["summary"]
    assert len(todo_entry.tags) == 1
    assert todo_entry.tags[0] == tag_text