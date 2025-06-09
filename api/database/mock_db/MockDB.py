from api.database.mock_db.MockDBQueue import MockDBQueue
from api.database.mock_db.MockDBRatings import MockDBRatings


class MockDB(MockDBQueue, MockDBRatings):

    pass