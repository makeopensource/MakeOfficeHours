"""Functions to handle authentication operations"""

from api.database.db import db


def create_account(username, numeric_identifier, auth_level="student"):
    """Creates an account with the specified information. Does
    not create a sign-in. Also adds this account to the roster.

    :param username: the username of the account to add
    :param numeric_identifier: a numeric identifier for this account. used by the card swipe
    :param auth_level: the authentication level.
    :return: the id of the newly created account.
    """

    account_id = db.create_account(username, numeric_identifier)
    db.add_to_roster(account_id, auth_level)
    return account_id


def get_user(cookies):
    """Gets the user account associated with these cookies
    retrieved from a request.

    :param cookies: dict[str, str] of the request's cookies
    :return: A dict containing the user's information if such a user exists,
             none otherwise.
    """
    if "auth_token" not in cookies:
        return None

    return db.get_authenticated_user(cookies["auth_token"])
