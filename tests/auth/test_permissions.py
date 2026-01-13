import pytest
import os
from dotenv import load_dotenv

load_dotenv()

from api.database.db import db
from api.auth.controller import create_account
from api.roster.controller import min_level
from api.server import create_app

app = create_app()

all_account_data = [
    {"username": "jy123", "pn": "123456789"},
    {"username": "lucy5", "pn": "123456784"},
    {"username": "steve", "pn": "987654321"},
    {"username": "jimmy", "pn": "67676767"},
    {"username": "horse", "pn": "154345345"},
]


@pytest.fixture
def test_db():
    db.filename = "testing.sqlite"
    db.connect()
    yield
    db.connection.commit()
    if os.path.exists("testing.sqlite"):
        os.remove("testing.sqlite")


@pytest.fixture
def accounts():
    accounts = {}  # id : account
    for account_data in all_account_data:
        account_id = create_account(account_data["username"], account_data["pn"])
        account_data["id"] = account_id
        accounts[account_id] = account_data

    lucy5 = db.lookup_person_number("123456784")
    db.add_to_roster(lucy5["user_id"], "ta")

    jimmy = db.lookup_person_number("67676767")
    db.add_to_roster(jimmy["user_id"], "instructor")

    horse = db.lookup_person_number("154345345")
    db.add_to_roster(horse["user_id"], "admin")

    yield accounts


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


@app.route("/test-ta")
@min_level("ta")
def ta_only():
    return "I'm at least TA!", 200


@app.route("/test-instructor")
@min_level("instructor")
def ins_only():
    return "I'm at least an instructor!", 200


@app.route("/test-admin")
@min_level("admin")
def admin_only():
    return "I'm at least an admin!", 200


def test_ta_instructor_admin_permissions(test_db, client, accounts):
    client.post("/signup", data={"ubit": "lucy5", "password": "jimmy"})

    client.post("/login", data={"ubit": "lucy5", "password": "jimmy"})

    assert client.get("/test-ta").status_code == 200
    assert client.get("/test-instructor").status_code == 403
    assert client.get("/test-admin").status_code == 403

    client.post("/signup", data={"ubit": "jimmy", "password": "jimmy2"})

    client.post("/login", data={"ubit": "jimmy", "password": "jimmy2"})

    assert client.get("/test-ta").status_code == 200
    assert client.get("/test-instructor").status_code == 200
    assert client.get("/test-admin").status_code == 403

    client.post("/signup", data={"ubit": "horse", "password": "jimmy3"})

    client.post("/login", data={"ubit": "horse", "password": "jimmy3"})

    assert client.get("/test-ta").status_code == 200
    assert client.get("/test-instructor").status_code == 200
    assert client.get("/test-admin").status_code == 200


def test_ta_queue_permissions(test_db, client, accounts):

    response = client.post("/signup", data={"ubit": "lucy5", "password": "jimmy"})

    assert (
        response.get_json().get("message")
        != "You are not in the roster. If this is an error, please contact the course staff."
    )

    response = client.post("/login", data={"ubit": "lucy5", "password": "jimmy"})

    assert response.get_json().get("message") == "Successfully logged in"

    response = client.post("/enqueue-ta-override", json={"identifier": "steve"})

    assert response.status_code == 200

    response = client.get("/get-queue")
    assert response.status_code == 200
    assert len(response.get_json()) == 1

    response = client.post("/help-a-student")
    assert response.status_code == 200

    auth_token = client.get_cookie("auth_token")
    response = client.post("/signout")
    assert response.status_code == 200
    assert client.get_cookie("auth_token") is None

    client.set_cookie("auth_token", auth_token.value, max_age=10000000)
    response = client.post("/enqueue-ta-override", json={"identifier": "steve"})
    assert response.status_code == 403

    assert db.get_authenticated_user(auth_token.value) is None

    response = client.post("/help-a-student")
    assert response.status_code == 403

    client.post("/signup", data={"ubit": "steve", "password": "jimmy2"})

    response = client.post("/login", data={"ubit": "steve", "password": "jimmy2"})
    assert response.status_code == 200

    response = client.post("/help-a-student")
    assert response.status_code == 403
