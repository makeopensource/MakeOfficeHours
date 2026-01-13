import datetime

from api.database.idb_visits import IVisits


class RelationalDBVisits(IVisits):

    def __init__(self):
        super().__init__()

    def create_visit(self, student, ta, enqueue_time) -> int:
        with self.cursor() as cursor:
            visit_id = cursor.execute("""
                INSERT INTO visits (student_id, ta_id, enqueue_time) VALUES (
                ?, ?, ?)
                RETURNING visit_id
            """, (student, ta, enqueue_time)).fetchone()[0]

            return visit_id



    def end_visit(self, visit_id):
        # YYYY-MM-DD HH:MM:SS
        now = str(datetime.datetime.now().isoformat(' ', timespec="seconds"))

        with self.cursor() as cursor:
            cursor.execute("""
                UPDATE visits
                SET session_end = ?
                WHERE visit_id = ? AND session_end is null
            """)

