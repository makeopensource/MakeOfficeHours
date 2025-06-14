from abc import ABC, abstractmethod


class IQueue(ABC):

    @abstractmethod
    def enqueue_student(self, student):
        raise NotImplementedError()

    @abstractmethod
    def dequeue_student(self):
        raise NotImplementedError()
