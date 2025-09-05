from abc import ABC, abstractmethod


class IAccounts(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def create_account(self, ubit, pn):
        # Creates an account with the provided ubit and pn. Generates, and returns, a unique id for the new account
        raise NotImplementedError()
