from abc import ABC, abstractmethod


class IQueue(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def enqueue_student(self, student):
        raise NotImplementedError()

    @abstractmethod
    def enqueue_student_front(self, student):
        raise NotImplementedError()

    @abstractmethod
    def dequeue_student(self):
        raise NotImplementedError()

    @abstractmethod
    def get_queue(self):
        raise NotImplementedError()

    @abstractmethod
    def remove_student(self, student):
        raise NotImplementedError()

    @abstractmethod
    def clear_queue(self):
        raise NotImplementedError()

    @abstractmethod
    def set_reason(self, student, reason):
        raise NotImplementedError()

    @abstractmethod
    def move_to_end(self, student):
        raise NotImplementedError()

    @abstractmethod
    def get_hw_authorization(self):
        raise NotImplementedError()

    @abstractmethod
    def reset_hw_authorization(self):
        raise NotImplementedError()