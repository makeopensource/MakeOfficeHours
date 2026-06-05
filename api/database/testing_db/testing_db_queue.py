"""Queue component of the testing DB"""

from api.database.idb_queue import IQueue
from api.database.testing_db.testing_db_utils import users

class TestingDBQueue(IQueue):
    """Queue implemention for testing DB"""

    def __init__(self):
        super().__init__()
        self.queue = []

    def _lookup_student(self, ident):
        return self.lookup_identifier(ident)  # pylint: disable=no-member

    def enqueue_student_front(self, student):
        if (user := self._lookup_student(student)) != {}:
            self.queue.insert(0, user)

    def get_queue(self):
        pass

    def remove_student(self, student):
        pass

    def dequeue_specified_student(self, student_id):
        pass

    def clear_queue(self):
        pass

    def set_reason(self, student, reason):
        pass

    def move_to_end(self, student):
        pass

    def get_hw_authorization(self):
        pass

    def reset_hw_authorization(self):
        pass

    def enqueue_student(self, student):
        self.queue.append(student)

    def dequeue_student(self):
        return self.queue.pop(0)
