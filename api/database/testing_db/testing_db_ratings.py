from api.database.idb_ratings import IRatings


class TestingDBRatings(IRatings):

    def __init__(self):
        super().__init__()

    def rate_student(self, student, rating, feedback):
        pass
        # do database stuff
