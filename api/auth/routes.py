"""Authentication Blueprint for MOH"""

import json
import os
import urllib.parse

import requests

from flask import Blueprint, request, make_response, redirect
from api.database.db import db
from api.auth.autolab_oauth import get_authorization_url, handle_code_after_redirect
from api.utils.debug import debug_access_only

blueprint = Blueprint("auth", __name__)

#### Autolab Paths

@blueprint.route("/authorize", methods=["GET"])
def login_with_autolab():
    """
    Called when the user clicks login with Autolab. Starts the process on talking to Autolab to get an Oauth access token
    """
    return redirect(get_authorization_url(), code=302)


@blueprint.route("/callback", methods=["GET"])
def getting_code_from_autolab():
    """
    Next step in the OAuth proccess. We're getting an auth code from Autolab and need to cash it in for an access token and refresh token
    """
    print(request.args)
    code = request.args.get("code")
    state = request.args.get("state")
    # TODO: check cookie to match state to session
    session = "not_implemented"

    auth_token = handle_code_after_redirect(code, state, session)

    if not auth_token:
        res = make_response("You are not enrolled in this class. If you should be, email Paul. It's his fault", 401)
        return res

    res = make_response(redirect("/queue"))
    res.set_cookie(
        "auth_token", auth_token, max_age=int(2.592e6), httponly=True, secure=True
    )
    return res


### Universal Paths (Used regardless of auth provider)

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


### Password auth paths

@blueprint.route("/login", methods=["POST"])
@debug_access_only
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
@debug_access_only
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



# TODO: update preferred name

# TODO: account has UBIT (For AL lookups) and pn (For card swipes)
