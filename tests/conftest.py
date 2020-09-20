import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from sw_api.app import make_app
from sw_api.database import set_session

_connection = None


def basic_data(dbsession):
    pass


@pytest.fixture(autouse=True, scope="session")
def session():
    global _connection
    database_name = 'sqlite://'
    if database_exists(database_name):
        drop_database(database_name)
    create_database(database_name)
    engine = create_engine(database_name)
    _connection = engine.connect()
    dbsession = sessionmaker(bind=_connection)()

    yield type("", (), {})

    drop_database(database_name)
    engine.dispose()


@pytest.fixture(autouse=True)
def tst(session):
    set_session('sqlite:////tmp/test.db', engine=_connection)
    transaction = _connection.begin()
    sales = make_app(engine=_connection)

    transaction = _connection.begin()
    sales = make_app(engine=_connection)
    session.client = sales.test_client()
    yield session
    transaction.rollback()

