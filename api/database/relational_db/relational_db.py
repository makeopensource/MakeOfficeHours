"""An implementation of the database interface using SQLite."""

import os

from api.database.db_interface import DBInterface
from api.database.relational_db.relational_db_cursor import RelationalDBCursor

from api.database.relational_db.relational_db_queue import RelationalDBQueue
from api.database.relational_db.relational_db_accounts import RelationalDBAccounts
from api.database.relational_db.relational_db_sessions import RelationalDBSessions
from api.database.relational_db.relational_db_visits import RelationalDBVisits


class RelationalDB(
    DBInterface,
    RelationalDBAccounts,
    RelationalDBQueue,
    RelationalDBVisits,
    RelationalDBSessions,
):  # pylint: disable=too-many-ancestors
    """Implementation for the SQLite version of the database interface."""

    def __init__(self):
        super().__init__()
        self.db_version = 0
        self.filename = os.getenv("SQLITE_DB_PATH", "./moh.sqlite")
        self._initialize()
        self._migrate()

    def _initialize(self):
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
                    course_role VARCHAR(16),
                    last_swipe  TEXT
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
                    enqueue_reason TEXT,
                    dequeued BOOLEAN DEFAULT false
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
        """Creates new cursor. Use with statements to ensure connections are cleaned up."""
        return RelationalDBCursor(self)

    def connect(self):
        pass

    def _migrate(self):
        with self.cursor() as c:
            self.db_version = c.execute("PRAGMA user_version").fetchone()[0]
            for script in sorted(os.listdir("./api/database/relational_db/migrations")):
                if int(script.split("_")[0]) > self.db_version:
                    with open(
                        f"./api/database/relational_db/migrations/{script}",
                        "r",
                        encoding="utf-8",
                    ) as sc_file:
                        c.executescript(sc_file.read())
            self.db_version = c.execute("PRAGMA user_version").fetchone()[0]
