import os
import json

import pytest
from dotenv import load_dotenv

load_dotenv()

from api.server import create_app
from api.auth.controller import create_account


@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    create_account("hartloff", "123456789")
    with app.test_client() as client:
        yield client


def test_first_test(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_data() == b"Welcome to the homepage, you are currently in testing mode"


def test_that_needs_db(client):
    client.post('/enqueue-ta-override', json.dumps({"id": "hartloff"}))
    response = client.post('/help-a-student')
    assert response.get_data() == b"hartloff"

