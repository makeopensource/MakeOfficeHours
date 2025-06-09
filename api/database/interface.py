from abc import ABC, abstractmethod

from IQueue import IQueue
from IRatings import IRatings

class DBInterface(IQueue, IRatings, ABC):

    # All database implements must extend this class

    @abstractmethod
    def connect(self):
        pass