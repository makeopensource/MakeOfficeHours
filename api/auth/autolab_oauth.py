import os
import base64
import json
import random
import secrets
from urllib.parse import urlencode

import requests

from api.database.db import db

AUTOLAB_SECRET = os.getenv("AUTOLAB_SECRET", "client_secret")
AUTOLAB_ID = os.getenv("AUTOLAB_CLIENT_ID", "client_id")
REDIRECT_URI = os.getenv("AUTOLAB_CALLBACK", "callback")

def get_authorization_url():
    autolab_url = "https://autolab.cse.buffalo.edu/oauth/authorize?"
    params={
        "redirect_uri":REDIRECT_URI, 
        "client_id":AUTOLAB_ID, 
        "response_type":"code", 
        "state":"abc", 
        "scopes":"user_info"
        }
    for (name, value)  in params.items():
        autolab_url += name + "=" + value + "&"
    autolab_url = autolab_url[:-1]
    print(autolab_url)
    return autolab_url


def start_session():
    token = secrets.token_urlsafe(20)
    state = secrets.token_urlsafe(20)
    users_collection.insert_one({"token": token, "state": state})
    return [token, state]


def handle_code_after_redirect(code, state, session):
        token = cash_in_code_for_token(code)

        [users_email, users_name] = user_info(token)

        ubit = users_email.split("@")[0]
        user_profile = db.lookup_identifier(ubit)

        if not user_profile:
            return None

        auth_token = db.sign_in_with_autolab(user_profile["user_id"])
        
        return auth_token



def cash_in_code_for_token(code):
    token_url = "https://autolab.cse.buffalo.edu/oauth/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "client_id": AUTOLAB_ID,
        "client_secret": AUTOLAB_SECRET,
        "redirect_uri": REDIRECT_URI
    })

    response = requests.post(token_url, headers=headers, data=data)
    print(response)
    the_good_stuff = json.loads(response.content.decode())
    access_token = the_good_stuff.get("access_token")
    refresh_token = the_good_stuff.get("refresh_token")
    scope = the_good_stuff.get("scope")
    expires_in = the_good_stuff.get("expires_in")
    created_at = the_good_stuff.get("created_at")

    # users_collection.update_one({"token": token}, {"$set": the_good_stuff})

    return access_token


def cash_in_refresh_token_for_token(refresh_token, token):
    token_url = "https://autolab.cse.buffalo.edu/oauth/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = urlencode({
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    })

    response = requests.post(token_url, headers=headers, data=data)
    print(response)
    the_good_stuff = json.loads(response.content.decode())
    access_token = the_good_stuff.get("access_token")
    refresh_token = the_good_stuff.get("refresh_token")
    scope = the_good_stuff.get("scope")
    expires_in = the_good_stuff.get("expires_in")
    created_at = the_good_stuff.get("created_at")

    users_collection.update_one({"token": token}, {"$set": the_good_stuff})

    return access_token


def user_info(access_token):
    user_url = "https://autolab.cse.buffalo.edu/api/v1/user"
    headers = {
        "Authorization": "Bearer " + access_token
    }
    response = requests.get(user_url, headers=headers)
    print(response)
    user_data = json.loads(response.content.decode())
    email = user_data.get("email")
    first_name = user_data.get("first_name")
    last_name = user_data.get("last_name")
    # users_collection.update_one({"token": token}, {"$set": user_data})
    return [email, first_name + " " + last_name]


def check_token(token):
    user_record = users_collection.find_one({"token": token})
    if user_record and "email" in user_record:
        return [user_record.get("email"),
                user_record.get("first_name") + " " + user_record.get("last_name")]
    else:
        return [None, None]


# TODO: Use refresh tokens. For now, once the token expires you'll lose access and things will break

if __name__ == '__main__':
    pass
