"""Queue component of the testing DB"""

from api.database.idb_queue import IQueue

import api.database.testing_db.testing_db_utils as utils


class TestingDBQueue(IQueue):
    """Queue implemention for testing DB"""

    def __init__(self):
        super().__init__()
        self.queue = []

    def enqueue_student_front(self, student, course):
        if (user := utils.lookup_identifier(student)) != {}:
            self.queue.insert(0, user)

    def get_queue(self, course):
        return self.queue

    def remove_student(self, student, course):
        student = utils.lookup_identifier(student)
        if student == {}:
            return None

        return self.queue.remove(utils.lookup_identifier(student))

    def dequeue_specified_student(self, student_id, course):
        pass

    def clear_queue(self, course):
        pass

    def set_reason(self, student, reason, course):
        pass

    def move_to_end(self, student, course):
        pass

    def get_hw_authorization(self, course):
        pass

    def reset_hw_authorization(self, course):
        pass

    def enqueue_student(self, student, course):
        self.queue.append(student)

    def dequeue_student(self, course):
        return self.queue.pop(0)
