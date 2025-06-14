from abc import ABC, abstractmethod

from api.database.idb_queue import IQueue
from api.database.idb_ratings import IRatings
from api.database.idb_accounts import IAccounts
from api.database.idb_roster import IRoster


class DBInterface(IQueue, IRatings, IAccounts, IRoster, ABC):

    # All database implements must extend this class

    @abstractmethod
    def connect(self):
        pass
