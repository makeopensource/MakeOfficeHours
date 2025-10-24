from api.database.db_interface import DBInterface

from api.database.relational_db.relational_db_queue import RelationalDBQueue
from api.database.relational_db.relational_db_ratings import RelationalDBRatings


class RelationalDB(DBInterface, RelationalDBQueue, RelationalDBRatings):
    pass
