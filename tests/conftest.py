import os

import pytest

from demo.database import Base
from tests.database import engine


@pytest.fixture(scope='session', autouse=True)
def setup_database():
    Base.metadata.create_all(engine)
    yield
    os.remove('test_database.sqlite')
