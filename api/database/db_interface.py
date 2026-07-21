"""The complete database interface. Split into multiple classes for readability."""

# pylint: disable=duplicate-code
from abc import ABC, abstractmethod

from api.database.idb_courses import ICourses
from api.database.idb_queue import IQueue
from api.database.idb_accounts import IAccounts
from api.database.idb_roster import IRoster
from api.database.idb_sessions import ISessions


class DBInterface(IQueue, IAccounts, IRoster, ISessions, ICourses, ABC):
    """The combined database interface.
    All database implements must extend this class"""

    @abstractmethod
    def connect(self):
        """Connect to the database. May not do anything based on implementation."""
