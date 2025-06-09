from api.database.IRatings import IRatings


class TestingDBRatings(IRatings):

    def rate_student(self, student, rating, feedback):
        pass
        # do database stuff