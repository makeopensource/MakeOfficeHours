from api.database.IQueue import IQueue


class RelationalDBQueue(IQueue):

    def enqueue_student(self, student):
        raise NotImplementedError()
        # do database stuff


    def dequeue_student(self):
        pass