"""test implementation of the database."""

from api.database.db_interface import DBInterface

from api.database.testing_db.testing_db_queue import TestingDBQueue
from api.database.testing_db.testing_db_accounts import TestingDBAccounts
from api.database.testing_db.testing_db_visits import TestingDBVisits


class TestingDB(
    DBInterface, TestingDBQueue, TestingDBAccounts, TestingDBVisits
):  # pylint: disable=too-many-ancestors
    """Definition of the full TestingDB"""

    def connect(self):
        pass
