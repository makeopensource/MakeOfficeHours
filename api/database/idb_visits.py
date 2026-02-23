from abc import ABC, abstractmethod

class IVisits(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def create_visit(self, student, ta, enqueue_time, visit_reason) -> int:
        """Create a database entry for the ongoing visit
        between the specified student and TA.

        enqueue_time should be in format "YYYY-MM-DD HH:MM:SS"
        Should indicate the time the visit was created

        :param student: The user ID of the student
        :param ta: The user ID of the TA
        :param enqueue_time: Timestamp when the student joined the queue,
                             in the format "YYYY-MM-DD HH:MM:SS"
        :param visit_reason: Student-supplied reason for joining the queue
        :return: A numeric ID representing the specific visit
        """
        raise NotImplementedError()

    @abstractmethod
    def end_visit(self, visit_id, reason):
        """Mark in the database that the specified visit
        has ended.

        :param visit_id: The numeric ID representing the specific visit
        :param reason:   The resolution of the visit
        """
        raise NotImplementedError()

    @abstractmethod
    def cancel_visit(self, visit_id):
        """ Destroy this visit from the database if it's still in progress.
        Un-dequeue this student from the queue if they have been dequeued.

        :param visit_id:
        :return:
        """


        raise NotImplementedError()

    @abstractmethod
    def get_in_progress_visits(self):
        """ Return all database entries for visits that have
        not ended.


        :return:
        """
        raise NotImplementedError()