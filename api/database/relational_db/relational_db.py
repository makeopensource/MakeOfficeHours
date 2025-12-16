import sqlite3

from api.database.db_interface import DBInterface
from api.database.relational_db.relational_db_cursor import RelationalDBCursor

from api.database.relational_db.relational_db_queue import RelationalDBQueue
from api.database.relational_db.relational_db_accounts import RelationalDBAccounts
from api.database.relational_db.relational_db_ratings import RelationalDBRatings


class RelationalDB(
    DBInterface, RelationalDBAccounts, RelationalDBQueue, RelationalDBRatings
):

    def __init__(self):
        super().__init__()
        self.filename = "../moh.sqlite"
        self.initialize()

    def initialize(self):
        with self.cursor() as c:
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS users
                (
                    user_id
                    INTEGER
                    PRIMARY
                    KEY,
                    preferred_name
                    VARCHAR
                (
                    64
                ),
                    last_name VARCHAR
                (
                    64
                ),
                    ubit VARCHAR
                (
                    16
                ) UNIQUE,
                    person_num INTEGER UNIQUE,
                    course_role VARCHAR
                (
                    16
                )
                    );
                """
            )

            c.execute(
                """
                CREATE TABLE IF NOT EXISTS queue
                (
                    user_id
                    INTEGER
                    UNIQUE,
                    joined
                    TEXT
                    DEFAULT (
                    datetime
                (
                    'now',
                    'localtime'
                ))
                    );
                """
            )

            c.execute(
                """
                CREATE TABLE IF NOT EXISTS auth
                (
                    user_id
                    INTEGER
                    UNIQUE,
                    auth_token
                    VARCHAR
                (
                    255
                ),
                    pw VARCHAR
                (
                    255
                ),
                    expires_at TEXT DEFAULT
                (
                    datetime
                (
                    'now',
                    '+30 days'
                ))
                    );
                """
            )

            c.execute(
                """
                CREATE TABLE IF NOT EXISTS visits
                (
                    visit_id
                    INTEGER
                    PRIMARY
                    KEY,
                    student_id
                    INTEGER,
                    ta_id
                    INTEGER,
                    session_start
                    TEXT
                    DEFAULT (
                    datetime
                (
                    'now',
                    'localtime'
                )),
                    session_end TEXT,
                    session_end_reason TEXT,
                    enqueue_time TEXT
                    );
                """
            )

    def cursor(self):
        return RelationalDBCursor(self)

    def connect(self):
        pass

    def add_to_roster(self, user_id, role):

        with self.cursor() as cursor:
            cursor.execute(
                """
                UPDATE users
                SET course_role = ?
                WHERE user_id = ?
                """,
                (role, user_id),
            )


