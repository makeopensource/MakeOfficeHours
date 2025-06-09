from api.database.IQueue import IQueue


class MockDBQueue(IQueue):

    def enqueue_student(self, student):
        pass
        # do database stuff