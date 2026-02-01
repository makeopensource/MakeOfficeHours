"""Authentication Blueprint for MOH"""

import json
import urllib.parse
import requests

from flask import Blueprint, request, make_response
from api.database.db import db
from api.auth.controller import AUTOLAB_ID, AUTOLAB_SECRET, REDIRECT_URI

blueprint = Blueprint("auth", __name__)


@blueprint.route("/login", methods=["POST"])
def login():
    """Checks if the current user has the right credentials to log in
    Args:
        ubit: form data field of ubit
        password: form data field of password

    Returns:
        The status of the login attempt
    """

    ubit = request.form.get("ubit")
    pw = request.form.get("password")

    auth_token = db.sign_in(ubit, pw)

    if not auth_token:
        return {"message": "Incorrect username or password"}, 400

    res = make_response(json.dumps({"message": "Successfully logged in"}), 200)
    res.content_type = "application/json"
    res.set_cookie(
        "auth_token", auth_token, max_age=int(2.592e6), httponly=True, secure=True
    )

    return res


@blueprint.route("/signup", methods=["POST"])
def signup():
    """Creates an account using the given credentials,
    fails if ubit already registered for an account
    or if ubit is not in the roster
    Args:
        ubit: forum data field of ubit
        password: forum data field of password

    Returns:
        The status of the sign-up attempt
    """

    ubit = request.form.get("ubit")
    pw = request.form.get("password")

    if not db.lookup_identifier(ubit):
        return {
            "message": "You are not in the roster. If this is an error, please contact the course staff."
        }, 400

    if not (auth_token := db.sign_up(ubit, pw)):
        return {"message": "Sign-in already exists"}, 400

    res = make_response(json.dumps({"message": "Successfully created account"}), 200)
    res.content_type = "application/json"
    res.set_cookie(
        "auth_token", auth_token, max_age=int(2.592e6), httponly=True, secure=True
    )
    return res


@blueprint.route("/signout", methods=["POST"])
def signout():
    """Signs out the currently logged-in user, invalidating their auth token
    Args:
        Request.cookie: the auth token of the currently logged-in user

    Returns:
        400 if no auth token is set
        200 on success
    """

    auth_token = request.cookies.get("auth_token")

    if not auth_token:
        return {"message": "You are not logged in."}, 400

    db.sign_out(auth_token)

    res = make_response(json.dumps({"message": "Logged out"}), 200)
    res.content_type = "application/json"
    res.set_cookie("auth_token", "", max_age=0, httponly=True, secure=True)

    return res


# TODO: update preferred name

# TODO: account has UBIT (For AL lookups) and pn (For card swipes)
