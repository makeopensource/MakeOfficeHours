import sqlite3

from api.database.db_interface import DBInterface

from api.database.relational_db.relational_db_queue import RelationalDBQueue
from api.database.relational_db.relational_db_accounts import RelationalDBAccounts
from api.database.relational_db.relational_db_ratings import RelationalDBRatings


class RelationalDB(DBInterface, RelationalDBAccounts, RelationalDBQueue, RelationalDBRatings):

    def __init__(self):
        super().__init__()
        self.connection = None
        self.cursor = None
        self.filename = "moh.sqlite"
        self.connect()


    def connect(self):
        self.connection = sqlite3.connect(self.filename)
        self.cursor = self.connection.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                preferred_name VARCHAR(64),
                last_name VARCHAR(64),
                ubit VARCHAR(16) UNIQUE,
                person_num INTEGER UNIQUE,
                course_role VARCHAR(16)
            );
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS queue (
                user_id INTEGER UNIQUE,
                joined TEXT DEFAULT (datetime('now', 'localtime'))
            );
        ''')

        self.connection.commit()

    def add_to_roster(self, user_id, role):
        self.cursor.execute('''
            UPDATE users
            SET course_role = ? WHERE user_id = ?
        ''', (role, user_id))
        self.cursor.commit()


