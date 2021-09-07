from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings


@event.listens_for(Engine, 'connect')
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON')
    cursor.close()


engine = create_engine(
    settings.database_url,
    future=True,
    connect_args={'check_same_thread': False},
)


Session = sessionmaker(engine, future=True)


def get_session() -> Session:
    with Session() as session:
        yield session


Base = declarative_base()
from .accounts.models import Account  # noqa
