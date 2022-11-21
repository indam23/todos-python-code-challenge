import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from persistence.db.base import Base


class DbAccessLayer:
    def __init__(self, engine):
        self.engine = engine
        Base.metadata.create_all(self.engine)

    def session(self):
        return sessionmaker(bind=self.engine, expire_on_commit=False)()


def get_postgres_db_engine_from_env():
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = os.environ.get("POSTGRES_HOST", "5432")
    database = os.environ.get("POSTGRES_HOST", "todo_challenge")
    engine = create_engine(f"postgresql://{host}:{port}/{database}")
    return engine
