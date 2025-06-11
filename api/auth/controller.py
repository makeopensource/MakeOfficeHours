from api.database.db import db

def create_account(username, numeric_identifier, auth_level='student'):
    db.create_account(username, numeric_identifier)
    pass
