"""Helper to create and cleanup cursors to access the database"""

import sqlite3


class RelationalDBCursor:
    """Class defining a cursor. Stores a connection and handles cleanup
    after use (committing changes and closing the connection)
    """

    def __init__(self, db):
        self.db = db
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db.filename)
        self.connection.row_factory = sqlite3.Row
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.commit()
        self.connection.close()
