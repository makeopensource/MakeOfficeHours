from abc import ABC, abstractmethod


class IRatings(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def rate_student(self, student, rating, feedback):
        raise NotImplementedError()
