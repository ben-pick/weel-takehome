import pytest
from takehome.app import app
@pytest.fixture(scope='session')
def client():
    app.config.update({"TESTING": True})

    with app.test_client() as client:
        yield client
