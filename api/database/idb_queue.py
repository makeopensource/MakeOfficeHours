"""The queue component of the database interface"""

from abc import ABC, abstractmethod


class IQueue(ABC):
    """Definitions for the database's queue interface"""

    @abstractmethod
    def enqueue_student(self, student):
        """Add the specified student to the end of the queue.

        :param student: Identifier for the student to add
        """
        raise NotImplementedError()

    @abstractmethod
    def enqueue_student_front(self, student):
        """Add the specified student to the front of the queue.

        :param student: Identifier for the student to add
        """
        raise NotImplementedError()

    @abstractmethod
    def dequeue_student(self):
        """Remove the student at the front of the queue
        from the queue.


        :return: The student's information, the visit reason,
        and visit time in a dict.
        {
            "user_id": <user id>,
            "preferred_name": <preferred name>,
            "ubit": <ubit>,
            "person_num": <person number>,
            "enqueue_time": <enqueue time>,
            "enqueue_reason": <enqueue reason>,
        }
        """

        raise NotImplementedError()

    @abstractmethod
    def get_queue(self):
        """Retrieve the queue.

        :return: The queue as a list of dicts matching
        {
            "id": <user id>,
            "preferred_name": <preferred name>,
            "ubit": <ubit>,
            "pn": <person number>,
        }
        """
        raise NotImplementedError()

    @abstractmethod
    def remove_student(self, student):
        """Remove the specified student from the queue

        :param student: The student's user id
        :return: The student's ID and join time in a dict:
                 {
                     "user_id": <user's ID>,
                     "joined": <user's join time>
                 }
                 None on failure
        """
        raise NotImplementedError()

    @abstractmethod
    def dequeue_specified_student(self, student_id):
        """Remove the specified student from the queue

        :param student_id: The user ID of the student to dequeue
        :return: The same information as dequeue_student
        """
        raise NotImplementedError()

    @abstractmethod
    def clear_queue(self):
        """Removes all students from the queue."""
        raise NotImplementedError()

    @abstractmethod
    def set_reason(self, student, reason):
        """Marks the student's reason for joining the queue

        :param student: the student whose reason to change
        :param reason: the user specified reason for joining
        """
        raise NotImplementedError()

    @abstractmethod
    def move_to_end(self, student):
        """Move the specified student to the end of the queue

        :param student: ID of the student to move
        :return: True on success, False on failure
        """
        raise NotImplementedError()

    @abstractmethod
    def get_hw_authorization(self):
        """Retrieves the authorization code for the card swipe

        :return: the authorization code
        """
        raise NotImplementedError()

    @abstractmethod
    def reset_hw_authorization(self):
        """Resets the hardware authorization code
        and generates a new, random one,

        :return: The newly generated code.
        """
        raise NotImplementedError()
