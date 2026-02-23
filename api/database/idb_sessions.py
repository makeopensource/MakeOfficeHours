from abc import ABC, abstractmethod


class ISessions(ABC):

    @abstractmethod
    def update_swipe_time(self, user):
        """ Update time user was enqueued to current time """
        raise NotImplementedError()

    @abstractmethod
    def reset_swipe_time(self, user):
        """ Reset time user was enqueued """
        raise NotImplementedError()

    @abstractmethod
    def get_swipe_time(self, user):
        """ Return time user was enqueued """
        raise NotImplementedError()

    @abstractmethod
    def get_on_site(self):
        """ Return list of students who have swiped in <= 2 hours
            who are not currently in the queue
        """
        raise NotImplementedError()

    @abstractmethod
    def clear_on_site(self):
        """ Reset everyone's last enqueue time """
        raise NotImplementedError()
