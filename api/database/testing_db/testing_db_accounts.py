"""Accounts/roster component of the testing DB"""

import secrets

from api.database.idb_accounts import IAccounts
from api.database.idb_roster import IRoster
from api.database.testing_db.testing_db_utils import users

import api.database.testing_db.testing_db_utils as utils


class TestingDBAccounts(IAccounts, IRoster):
    """Implementations for the accounts and roster methods"""

    def save_autolab_info(self, user_id, access_token, refresh_token, expires_in):
        pass

    def get_autolab_info(self, user_id):
        pass

    def get_enrollments(self, user_id):
        pass

    def remove_from_roster(self, user_id, course):
        pass

    def clear_students(self, course):
        pass

    def create_account(self, ubit, pn, role="user"):
        users.append({"ubit": ubit, "person_num": pn})

    def lookup_person_number(self, person_number, course=None) -> dict[str, str]:
        return utils.lookup_person_number(person_number)

    def lookup_identifier(self, identifier, course=None) -> dict[str, str]:
        return utils.lookup_identifier(identifier)

    def get_authenticated_user(self, auth_token, course=None) -> dict[str, str]:
        for user in users:
            if user["auth"] == auth_token:
                return user
        return {}

    def sign_up(self, username, pw) -> str | None:
        for user in users:
            if user["ubit"] == username:
                user["pw"] = pw
                user["auth"] = secrets.token_urlsafe()
                return user["auth"]
        return None

    def sign_in(self, username, pw) -> str | None:
        for user in users:
            if user["ubit"] == username and user["pw"] == pw:
                user["auth"] = secrets.token_urlsafe()
                return user["auth"]
        return None

    def sign_in_with_autolab(self, ubit) -> str | None:
        for user in users:
            if user["ubit"] == ubit:
                user["auth"] = secrets.token_urlsafe()
                return user["auth"]
        return None

    def sign_out(self, auth_token):
        for user in users:
            if user["auth"] == auth_token:
                user["auth"] = "nah"
                return

    def set_preferred_name(self, identifier, name):
        user = self.lookup_identifier(identifier)
        if user is not None:
            user["fn"] = name

    def set_initial_name(self, user_id, first_name, last_name):
        user = self.lookup_identifier(user_id)
        if user is not None:
            user["fn"] = first_name
            user["sn"] = last_name

    def add_to_roster(self, user_id, role, course):
        user = self.lookup_identifier(user_id)
        if user is not None and role in {"student", "ta", "instructor", "admin"}:
            user["course_role"] = role

    def get_roster(self, course):
        return users

    def delete_user(self, user_id):
        pass
