import datetime

from api.database.idb_visits import IVisits


class RelationalDBVisits(IVisits):

    def __init__(self):
        super().__init__()

    def create_visit(self, student, ta, enqueue_time, visit_reason) -> int:
        with self.cursor() as cursor:
            visit_id = cursor.execute("""
                INSERT INTO visits (student_id, ta_id, enqueue_time, student_visit_reason) VALUES (
                ?, ?, ?, ?)
                RETURNING visit_id
            """, (student, ta, enqueue_time, visit_reason)).fetchone()[0]

            return visit_id



    def end_visit(self, visit_id, reason):
        # YYYY-MM-DD HH:MM:SS
        now = str(datetime.datetime.now().isoformat(' ', timespec="seconds"))

        with self.cursor() as cursor:
            cursor.execute("""
                UPDATE visits
                SET session_end = ?, session_end_reason = ?
                WHERE visit_id = ? AND session_end is null
            """, (now, reason, visit_id))

