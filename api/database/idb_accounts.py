from abc import ABC, abstractmethod


class IAccounts(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def create_account(self, ubit, pn):
        # Creates an account with the provided ubit and pn. Generates, and returns, a unique id for the new account
        raise NotImplementedError()

    @abstractmethod
    def lookup_person_number(self, person_number) -> dict[str, str]:
        # Returns the database entry for the user with the specified person number.
        raise NotImplementedError()

    @abstractmethod
    def lookup_identifier(self, identifier) -> dict[str, str]:
        # Returns the database entry for the user with the specified identifier.
        # resolves UBIT -> person number -> unique id
        raise NotImplementedError()