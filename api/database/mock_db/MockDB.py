from api.database.interface import DBInterface


class MockDB(DBInterface):

    def connect(self):
        pass

    def enqueue_student(self, student):
        pass

    def dequeue_student(self):
        pass

    def rate_student(self, student, rating, feedback):
        pass

    def create_account(self, ubit, pn):
        pass

    def add_to_roster(self, user_id, role):
        pass