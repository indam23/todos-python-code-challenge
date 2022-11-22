import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from entities import TodoEntry
from persistence.db.base import Base
from persistence.db.db_access import DbAccessLayer
from persistence.mapper.sql import SqlTodoEntryMapper

from tests.conftest import EXISTING_TODO_DATA, NEW_TODO_DATA


@pytest.fixture
def engine():
    return create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)

@pytest.fixture
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture
def session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=engine, expire_on_commit=False)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def sql_mapper(engine):
    return SqlTodoEntryMapper(DbAccessLayer(engine))


@pytest.fixture()
def existing_todo(sql_mapper, session):
    sql_mapper.create_todo(TodoEntry(**EXISTING_TODO_DATA), session)


@pytest.fixture()
def new_todo_entry():
    data = {k:v for k,v in NEW_TODO_DATA.items() if k != "id"}
    todo_entry = TodoEntry(**data)
    return todo_entry

@pytest.fixture()
def existing_todo_entry():
    todo_entry = TodoEntry(**EXISTING_TODO_DATA)
    return todo_entry