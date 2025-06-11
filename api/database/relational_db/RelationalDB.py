from api.database.interface import DBInterface

from api.database.relational_db.RelationalDBQueue import RelationalDBQueue
from api.database.relational_db.RelationalDBRatings import RelationalDBRatings


class RelationalDB(DBInterface, RelationalDBQueue, RelationalDBRatings):

    pass