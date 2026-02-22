from abc import ABC, abstractmethod

from api.database.idb_queue import IQueue
from api.database.idb_ratings import IRatings
from api.database.idb_accounts import IAccounts
from api.database.idb_roster import IRoster
from api.database.idb_sessions import ISessions


class DBInterface(IQueue, IRatings, IAccounts, IRoster, ISessions, ABC):

    # All database implements must extend this class

    def __init__(self):
        super().__init__()

    @abstractmethod
    def connect(self):
        pass
