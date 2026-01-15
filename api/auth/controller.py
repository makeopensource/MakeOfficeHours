from api.database.db import db
import os

AUTOLAB_SECRET = os.getenv("AUTOLAB_CLIENT_SECRET")
AUTOLAB_ID = os.getenv("AUTOLAB_CLIENT_ID")
REDIRECT_URI = os.getenv("AUTOLAB_REDIRECT_URI")

def create_account(username, numeric_identifier, auth_level="student"):
    account_id = db.create_account(username, numeric_identifier)
    db.add_to_roster(account_id, auth_level)
    return account_id

def get_user(cookies):
    if "auth_token" not in cookies:
            return None

    return db.get_authenticated_user(cookies["auth_token"])


