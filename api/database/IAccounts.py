
from abc import ABC, abstractmethod

class IAccounts:

    @abstractmethod
    def create_account(self, ubit, pn):
        # return id
        raise NotImplementedError()