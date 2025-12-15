import os

from api.database.relational_db.relational_db import RelationalDB
from api.database.testing_db.testing_db import TestingDB
from api.database.mock_db.mock_db import MockDB


def create_db():
    db_type = os.getenv("DB")
    match db_type:
        case "relational":
            return RelationalDB()
        case "testing":
            return TestingDB()
        case "mock":
            return MockDB()
        case None:
            raise EnvironmentError('environment variable "DB" not set')
        case _:
            raise ModuleNotFoundError("Could not find database named " + db_type)


db = create_db()
