from abc import ABC, abstractmethod


class IRatings:

    @abstractmethod
    def rate_student(self, student, rating, feedback):
        raise NotImplementedError()
