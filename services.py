import database as _database


def create_db():
    return _database.Base.metadata.create_all(bind=_database.engine)


create_db()
