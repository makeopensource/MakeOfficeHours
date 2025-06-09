from api.database.IRatings import IRatings


class MockDBRatings(IRatings):

    def rate_student(self, student, rating, feedback):
        pass
        # do database stuff