from api.database.interface import DBInterface

from api.database.testing_db.TestingDBQueue import TestingDBQueue
from api.database.testing_db.TestingDBRatings import TestingDBRatings


class TestingDB(DBInterface, TestingDBQueue, TestingDBRatings):

    def connect(self):
        pass

    def create_account(self, ubit, pn):
        print("Welcome " + ubit)

    def add_to_roster(self, user_id, role):
        pass

