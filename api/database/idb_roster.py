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