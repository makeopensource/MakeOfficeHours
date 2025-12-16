from api.database.db import db


def create_account(username, numeric_identifier, auth_level="student"):
    account_id = db.create_account(username, numeric_identifier)
    print(auth_level)
    db.add_to_roster(account_id, auth_level)
    return account_id
