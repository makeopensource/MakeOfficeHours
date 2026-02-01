from abc import ABC, abstractmethod


class IRoster(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def add_to_roster(self, user_id, role):
        raise NotImplementedError()

    @abstractmethod
    def get_roster(self):
        raise NotImplementedError()