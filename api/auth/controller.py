from api.database.db import db


def create_account(username, numeric_identifier, auth_level='student'):
    account_id = db.create_account(username, numeric_identifier)
    return account_id
