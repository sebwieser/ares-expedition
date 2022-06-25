import pytest
from flask.testing import FlaskClient
from aresexpedition import create_app


@pytest.fixture
def client() -> FlaskClient:
    a = create_app(test=True)
    return a.test_client()


def test_homepage(client: FlaskClient):
    res = client.get('/')
    assert b'Terraforming Mars: Ares Expedition' in res.data.title()
