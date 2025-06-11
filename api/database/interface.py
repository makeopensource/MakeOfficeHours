from abc import ABC, abstractmethod

from api.database.IQueue import IQueue
from api.database.IRatings import IRatings
from api.database.IAccounts import IAccounts
from api.database.IRoster import IRoster

class DBInterface(IQueue, IRatings, IAccounts, IRoster, ABC):

    # All database implements must extend this class

    @abstractmethod
    def connect(self):
        pass