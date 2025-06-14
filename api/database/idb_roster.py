
from abc import ABC, abstractmethod

class IRoster:

    @abstractmethod
    def add_to_roster(self, user_id, role):
        raise NotImplementedError()

