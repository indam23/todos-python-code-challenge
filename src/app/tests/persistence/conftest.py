import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from entities import TodoEntry
from persistence.db.base import Base
from persistence.db.db_access import DbAccessLayer
from persistence.mapper.persistent import SqlTodoEntryMapper

from tests.conftest import EXISTING_TODO_DATA


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


class MockDbAccessLayer(DbAccessLayer):
    def session(self):
        return session()


@pytest.fixture
def sql_mapper():
    return SqlTodoEntryMapper(MockDbAccessLayer)


@pytest.fixture()
def existing_todo(sql_mapper, session):
    sql_mapper.create_todo(TodoEntry(**EXISTING_TODO_DATA), session)
