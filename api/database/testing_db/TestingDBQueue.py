from api.database.IQueue import IQueue


class TestingDBQueue(IQueue):

    def __init__(self):
        self.queue = []

    def enqueue_student(self, student):
        self.queue.append(student)

    def dequeue_student(self):
        return self.queue.pop(0)