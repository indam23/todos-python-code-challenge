from persistence.mapper.sql import SqlTodoEntryMapper
from persistence.db.db_access import DbAccessLayer, get_postgres_db_engine_from_env


def init_mapper():
    db = DbAccessLayer(get_postgres_db_engine_from_env())
    mapper = SqlTodoEntryMapper(db)
    return mapper
