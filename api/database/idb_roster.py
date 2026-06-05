"""The roster component of the database interface"""

from abc import ABC, abstractmethod


class IRoster(ABC):
    """Definitions for the roster component of the database interface"""

    @abstractmethod
    def add_to_roster(self, user_id, role):
        """Set the user with id user_id to have the role
        specified by role.

        :param user_id: The user_id of the user
        :param role: The desired role.
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def get_roster(self):
        """Retrieve the entire roster and their
        relevant information from the database.

        :return: The roster as a list of dicts like:
                    {
                        "user_id",
                        "preferred_name",
                        "last_name",
                        "ubit",
                        "person_num",
                        "course_role",
                    }
        """
        raise NotImplementedError()

    # @abstractmethod
    # def get_matched_student(self, query) -> list:
    #     """
    #     Find students matching query.
    #
    #
    #     :param query: Substring of either the student's
    #                   preferred name, last name, or username.
    #     :return: A list of student information as a dict
    #     """
    #     raise NotImplementedError()
