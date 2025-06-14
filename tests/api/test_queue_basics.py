import os
import json

import pytest
from dotenv import load_dotenv

load_dotenv()

from api.server import create_app
from api.auth.controller import create_account

all_account_data = [
    {"username": "jy123", "pn": "123456789"},
    {"username": "lucy5", "pn": "123456784"},
    {"username": "steve", "pn": "987654321"}
]

@pytest.fixture
def accounts():
    accounts = {} # id : account
    for account_data in all_account_data:
        account_id = create_account(account_data["username"], account_data["pn"])
        account_data["id"] = account_id
        accounts[account_id] = account_data
    yield accounts


@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client



def test_first_test(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_data() == b"Welcome to the homepage, you are currently in testing mode"


def test_that_needs_db(client, accounts):
    client.post('/enqueue-ta-override', json.dumps({"id": "lucy5"}))
    response = client.post('/help-a-student')
    assert response.get_data() == b"lucy5"

