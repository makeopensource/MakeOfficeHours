"""The account component of the database interface."""

# pylint: disable=duplicate-code
from abc import ABC, abstractmethod


class IAccounts(ABC):
    """Definitions for the accounts component of the database interface."""

    @abstractmethod
    def create_account(self, ubit, pn, role="user"):
        """Creates an account with the provided ubit and pn. Generates, and returns, a unique id for the new account"""
        raise NotImplementedError()

    @abstractmethod
    def lookup_person_number(self, person_number, course=None) -> dict[str, str]:
        """Returns the database entry for the user with the specified person number."""
        raise NotImplementedError()

    @abstractmethod
    def lookup_identifier(self, identifier, course=None) -> dict[str, str]:
        """Returns the database entry for the user with the specified identifier.
        resolves UBIT -> person number -> unique id
        """
        raise NotImplementedError()

    @abstractmethod
    def get_authenticated_user(self, auth_token, course=None) -> dict[str, str]:
        """Returns the database entry for the user with the specified auth token."""
        raise NotImplementedError()

    @abstractmethod
    def sign_up(self, username, pw) -> str | None:
        """creates a sign in for the requested user

        :param username: the user's username
        :param pw: the desired password
        :return:    None if the user's ubit isn't in the system
                    an auth token for the user, otherwise
        """

        raise NotImplementedError()

    @abstractmethod
    def sign_in(self, username, pw) -> str | None:
        """generates and returns a valid auth token for the user if the username and password match

        :param username: The username to check
        :param pw: The password to check
        :return: The generated auth token, on success
                 returns None on error
        """

        raise NotImplementedError()

    @abstractmethod
    def sign_in_with_autolab(self, ubit) -> str | None:
        """generates and returns a valid auth token for the user.
        Assumes Autolab already authenticated the user

        :param ubit: The ubit to generate an auth token for.
        :return: The generated auth token
                 None on error
        """
        raise NotImplementedError()

    @abstractmethod
    def sign_out(self, auth_token):
        """invalidates the specified auth token"""
        raise NotImplementedError()

    @abstractmethod
    def set_preferred_name(self, identifier, name):
        """set the user's preferred name based on identifier

        :param identifier: the identifier of the user
        :param name: the desired new name
        :return The user ID on success
                None if the user doesn't exist
        """

        raise NotImplementedError()

    @abstractmethod
    def set_initial_name(self, user_id, first_name, last_name):
        """Sets the user's full name based on identifier

        :param user_id: the user's id
        :param first_name: the user's desired first name
        :param last_name: the user's desired last name
        :return: The user ID on success
                 None if the user doesn't exist
        """

        raise NotImplementedError()

    @abstractmethod
    def delete_user(self, user_id):
        """Deletes the specified user. They must not be returned
        in other functions after this, except in historical visit
        records. These records must have some indication that
        the visit is "archived."

        :param user_id: The user id of the user to delete
        """
        raise NotImplementedError()

    @abstractmethod
    def get_enrollments(self, user_id):
        """Return all the courses the specified user is a member
        of, alongside the role.

        :param user_id: the user id to query
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def save_autolab_info(self, user_id, access_token, refresh_token, expires_in):
        """Stores the respective Autolab info in the user's database entry

        :param user_id: the user being updated
        :param access_token: the user's access token
        :param refresh_token: the user's refresh token
        :param expires_in: how many seconds until the token expires
        """
        raise NotImplementedError()

    @abstractmethod
    def get_autolab_info(self, user_id):
        """Gets the Autolab info from the specified user

        :param user_id: the specified user
        :return: dict containing:
        {
            "access_token": <the user's access token, or None if it is expired>
            "refresh_token": <the user's refresh token>
        }
                None if the user doesn't have Autolab set up
        """
        raise NotImplementedError()
