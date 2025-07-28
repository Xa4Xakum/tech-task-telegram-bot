from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import event
from sqlalchemy.engine import Engine

from config.init import conf

engine = create_engine(conf.db_conneciton, echo=False, pool_pre_ping=True)
SessionFactory = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class BaseCrud():
    '''базовый класс crud-методов'''

    def __init__(self, session: sessionmaker[Session]) -> None:
        self.session = session
