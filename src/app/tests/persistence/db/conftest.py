import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from persistence.db.base import Base
from persistence.db.db_access import DbAccessLayer


@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)

@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=engine, expire_on_commit=False)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

class MockDbAccessLayer(DbAccessLayer):
    def session():
        