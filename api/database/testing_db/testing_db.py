from api.database.db_interface import DBInterface

from api.database.testing_db.testing_db_queue import TestingDBQueue
from api.database.testing_db.testing_db_accounts import TestingDBAccounts


class TestingDB(DBInterface, TestingDBQueue, TestingDBAccounts):

    def dequeue_specified_student(self, student_id):
        pass

    def enqueue_student_front(self, student):
        pass

    def get_queue(self):
        pass

    def remove_student(self, student):
        pass

    def clear_queue(self):
        pass

    def set_reason(self, student, reason):
        pass

    def move_to_end(self, student):
        pass

    def get_hw_authorization(self):
        pass

    def reset_hw_authorization(self):
        pass

    def lookup_person_number(self, person_number) -> dict[str, str]:
        pass

    def lookup_identifier(self, identifier) -> dict[str, str]:
        pass

    def get_authenticated_user(self, auth_token) -> dict[str, str]:
        pass

    def sign_up(self, username, pw) -> str | None:
        pass

    def sign_in(self, username, pw) -> str | None:
        pass

    def sign_in_with_autolab(self, ubit) -> str | None:
        pass

    def sign_out(self, auth_token):
        pass

    def set_preferred_name(self, identifier, name):
        pass

    def set_name(self, identifier, first_name, last_name):
        pass

    def get_roster(self):
        pass

    def update_swipe_time(self, user):
        pass

    def reset_swipe_time(self, user):
        pass

    def get_swipe_time(self, user):
        pass

    def get_on_site(self):
        pass

    def clear_on_site(self):
        pass

    def __init__(self):
        super().__init__()

    def connect(self):
        pass

    def add_to_roster(self, user_id, role):
        pass
