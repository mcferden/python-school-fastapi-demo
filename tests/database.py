from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker


@event.listens_for(Engine, 'connect')
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON')
    cursor.close()


engine = create_engine(
    'sqlite:///test_database.sqlite',
    future=True,
    connect_args={'check_same_thread': False},
)


Session = sessionmaker(engine, future=True)


def get_session() -> Session:
    with Session() as session:
        yield session
