"""The roster component of the database interface"""

# pylint: disable=duplicate-code
from abc import ABC, abstractmethod


class IRoster(ABC):
    """Definitions for the roster component of the database interface"""

    @abstractmethod
    def add_to_roster(self, user_id, role, course):
        """Set the user with id user_id to have the role
        specified by role.

        :param user_id: The user_id of the user
        :param role: The desired role.
        :param course: the course to add to user to
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def get_roster(self, course):
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

    @abstractmethod
    def remove_from_roster(self, user_id, course):
        """Remove the specified user from the course

        :param user_id: the user to remove
        :param course: the course to remove from
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def clear_students(self, course):
        """Marks all students as deleted."""
        raise NotImplementedError

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
