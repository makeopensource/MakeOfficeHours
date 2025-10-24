from abc import ABC, abstractmethod


class IQueue(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def enqueue_student(self, student):
        raise NotImplementedError()

    @abstractmethod
    def dequeue_student(self):
        raise NotImplementedError()
