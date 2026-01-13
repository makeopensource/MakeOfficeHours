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

    @abstractmethod
    def get_authenticated_user(self, auth_token) -> dict[str, str]:
        # Returns the database entry for the user with the specified auth token.
        raise NotImplementedError()

    @abstractmethod
    def sign_up(self, username, pw) -> str | None:
        # creates a sign in for the requested user
        # returns None if the user's ubit isn't in the system
        # returns an auth token for the user
        raise NotImplementedError()

    @abstractmethod
    def sign_in(self, username, pw) -> str | None:
        # generates and returns a valid auth token for the user if the username and password match
        # returns None on error
        raise NotImplementedError()

    @abstractmethod
    def sign_out(self, auth_token):
        # invalidates the specified auth token
        raise NotImplementedError()

    @abstractmethod
    def set_preferred_name(self, identifier, name):
        # set the user's preferred name based on identifier
        raise NotImplementedError()