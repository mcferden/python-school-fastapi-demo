from fastapi.testclient import TestClient

from demo.accounts.models import Account
from demo.app import app
from demo.database import get_session
from tests.database import Session
from tests.database import get_session as get_test_session


app.dependency_overrides[get_session] = get_test_session
client = TestClient(app)


def test_get_account():
    # arrange
    url = '/get-account/1'

    with Session() as session:
        session.add(Account(
            email='test',
            username='test',
            password='test',
        ))
        session.commit()

    # act
    response = client.get(url)
    response_json = response.json()

    # assert
    assert response.status_code == 200
    assert response_json['id'] == 1
