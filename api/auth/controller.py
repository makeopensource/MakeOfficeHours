from api.database.db import db


def create_account(username, numeric_identifier, auth_level="student"):
    account_id = db.create_account(username, numeric_identifier)
    db.add_to_roster(account_id, auth_level)
    return account_id
