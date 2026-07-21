"""The user sessions component of the database interface"""

# pylint: disable=duplicate-code
from abc import ABC, abstractmethod


class ISessions(ABC):
    """Definitions for the user sessions component of the database interface."""

    @abstractmethod
    def update_swipe_time(self, user, course):
        """Update time user was last enqueued to current time.

        :param user: the user id of the user to refresh.
        """
        raise NotImplementedError()

    @abstractmethod
    def reset_swipe_time(self, user, course):
        """Reset time user was enqueued.

        :param course: the course the user is a part of
        :param user: the user id of the user
        """
        raise NotImplementedError()

    @abstractmethod
    def get_swipe_time(self, user, course):
        """Return time user was enqueued.

        :param course: the course the user is a part of
        :param user: the user id of the user
        :return: the timestamp of when the user last swiped formatted YYYY-MM-DD HH:MM:SS
                 None if the user has never swiped, or if it was reset
        """
        raise NotImplementedError()

    @abstractmethod
    def get_on_site(self, course):
        """Return list of students who have swiped in <= 2 hours
        who are not currently in the queue

        :return: list of active students.
        """
        raise NotImplementedError()

    @abstractmethod
    def clear_on_site(self, course):
        """Reset everyone's last enqueue time"""
        raise NotImplementedError()
