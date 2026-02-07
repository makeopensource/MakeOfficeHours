import os

from api.database.db_interface import DBInterface
from api.database.relational_db.relational_db_cursor import RelationalDBCursor

from api.database.relational_db.relational_db_queue import RelationalDBQueue
from api.database.relational_db.relational_db_accounts import RelationalDBAccounts
from api.database.relational_db.relational_db_ratings import RelationalDBRatings
from api.database.relational_db.relational_db_visits import RelationalDBVisits


class RelationalDB(DBInterface, RelationalDBAccounts, RelationalDBQueue, RelationalDBRatings, RelationalDBVisits):

    def __init__(self):
        super().__init__()
        self.filename = os.getenv("SQLITE_DB_PATH", "./moh.sqlite")
        self.initialize()

    def initialize(self):
        with self.cursor() as c:
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS users
                (
                    user_id INTEGER PRIMARY KEY,
                    preferred_name VARCHAR(255),
                    last_name VARCHAR(255),
                    ubit VARCHAR(16) UNIQUE,
                    person_num INTEGER UNIQUE,
                    course_role VARCHAR(16)
                );
                """
            )

            c.execute(
                """
                CREATE TABLE IF NOT EXISTS queue
                (
                    user_id INTEGER UNIQUE,
                    joined TEXT DEFAULT (datetime('now', 'localtime')),
                    priority INTEGER,
                    enqueue_reason TEXT
                );
                """
            )

            c.execute(
                """
                CREATE TABLE IF NOT EXISTS auth
                (
                    user_id INTEGER UNIQUE,
                    auth_token VARCHAR(255),
                    al_access_token VARCHAR(255),
                    al_refresh_token VARCHAR(255),
                    al_state VARCHAR(255),
                    al_session_id VARCHAR(255),
                    pw VARCHAR(255),
                    expires_at TEXT DEFAULT (datetime('now','+30 days'))
                );
                """
            )

            c.execute(
                """
                CREATE TABLE IF NOT EXISTS visits
                (
                    visit_id INTEGER PRIMARY KEY,
                    student_id INTEGER,
                    ta_id INTEGER,
                    student_visit_reason TEXT,
                    session_start TEXT DEFAULT (datetime('now','localtime')),
                    session_end TEXT,
                    session_end_reason TEXT,
                    enqueue_time TEXT
                    );
                """
            )

            c.execute(
                """
                CREATE TABLE IF NOT EXISTS hardware
                (
                    authorization VARCHAR(255),
                    expires_at TEXT DEFAULT (datetime('now', '+180 days'))
                );
                
                
                """
            )

    def cursor(self):
        return RelationalDBCursor(self)

    def connect(self):
        pass

