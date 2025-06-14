from api.database.db_interface import DBInterface

from api.database.testing_db.testing_db_queue import TestingDBQueue
from api.database.testing_db.testing_db_ratings import TestingDBRatings
from api.database.testing_db.testing_db_accounts import TestingDBAccounts


class TestingDB(DBInterface, TestingDBQueue, TestingDBRatings, TestingDBAccounts):

    def connect(self):
        pass

    def add_to_roster(self, user_id, role):
        pass
