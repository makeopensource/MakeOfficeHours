import sqlite3


class RelationalDBCursor:
    def __init__(self, db):
        self.db = db
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db.filename)
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.commit()
        self.connection.close()