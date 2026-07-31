"""Functions to handle authentication via Autolab"""

import os
import json
from urllib.parse import urlencode

import requests

from api.database.db import db
from api.student_data_lookups import autolab

AUTOLAB_SECRET = os.getenv("AUTOLAB_SECRET", "client_secret")
AUTOLAB_ID = os.getenv("AUTOLAB_CLIENT_ID", "client_id")
REDIRECT_URI = os.getenv("AUTOLAB_CALLBACK", "callback")


def get_authorization_url():
    """Generates the appropriate Autolab authorization URL based on the environment variables"""
    autolab_url = "https://autolab.cse.buffalo.edu/oauth/authorize?"
    params = {
        "redirect_uri": REDIRECT_URI,
        "client_id": AUTOLAB_ID,
        "response_type": "code",
        "state": "abc",
        "scopes": "user_info,user_courses",
    }
    for name, value in params.items():
        autolab_url += name + "=" + value + "&"
    autolab_url = autolab_url[:-1]
    return autolab_url


def handle_code_after_redirect(code):
    """Cashes in the code for a token and signs the user in"""
    token, refresh_token, expires_in = cash_in_code_for_token(code)

    if token is None:
        return None

    result = autolab.user_info(token)

    if not result:
        return None

    [users_email, _] = result

    ubit = users_email.split("@")[0]
    user_profile = db.lookup_identifier(ubit)

    if not user_profile:
        return None

    db.save_autolab_info(user_profile["user_id"], token, refresh_token, expires_in)
    auth_token = db.sign_in_with_autolab(user_profile["user_id"])
    return auth_token


def cash_in_code_for_token(code):
    """Obtains the user's token given a code"""
    token_url = "https://autolab.cse.buffalo.edu/oauth/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = urlencode(
        {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": AUTOLAB_ID,
            "client_secret": AUTOLAB_SECRET,
            "redirect_uri": REDIRECT_URI,
        }
    )
    try:
        response = requests.post(token_url, headers=headers, data=data, timeout=5.0)
    except requests.Timeout:
        return None
    the_good_stuff = json.loads(response.content.decode())
    access_token = the_good_stuff.get("access_token")
    refresh_token = the_good_stuff.get("refresh_token")
    # scope = the_good_stuff.get("scope")
    expires_in = the_good_stuff.get("expires_in")
    # created_at = the_good_stuff.get("created_at")

    return access_token, refresh_token, expires_in


def cash_in_refresh_token_for_token(refresh_token):
    """Get a new access token and refresh token given a refresh token.

    @param refresh_token: The refresh token to cash in.
    """
    token_url = "https://autolab.cse.buffalo.edu/oauth/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = urlencode({"grant_type": "refresh_token", "refresh_token": refresh_token})

    response = requests.post(token_url, headers=headers, data=data, timeout=5.0)
    the_good_stuff = json.loads(response.content.decode())
    access_token = the_good_stuff.get("access_token")
    refresh_token = the_good_stuff.get("refresh_token")
    expires_in = the_good_stuff.get("expires_in")

    return access_token, refresh_token, expires_in


# def check_token(token):
#     user_record = users_collection.find_one({"token": token})
#     if user_record and "email" in user_record:
#         return [
#             user_record.get("email"),
#             user_record.get("first_name") + " " + user_record.get("last_name"),
#         ]
#     else:
#         return [None, None]


# TODO: Use refresh tokens. For now, once the token expires you'll lose access and things will break
