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

            student = cursor.execute("SELECT (student_id) from visits WHERE visit_id = ?", (visit_id, )).fetchone()

            if student is None:
                return

            student = student[0]

            cursor.execute("""
                UPDATE visits
                SET session_end = ?, session_end_reason = ?
                WHERE visit_id = ? AND session_end is null
            """, (now, reason, visit_id))

        self.remove_student(student)

    def cancel_visit(self, visit_id):
        with self.cursor() as cursor:

            student = cursor.execute("SELECT (student_id) from visits WHERE visit_id = ?", (visit_id,)).fetchone()

            if student is None:
                return

            student = student[0]

            cursor.execute("DELETE from visits WHERE visit_id = ?", (visit_id,))

            cursor.execute("UPDATE queue SET dequeued = false WHERE user_id = ?", (student, ))


    def get_in_progress_visits(self):
        with self.cursor() as cursor:
            result = cursor.execute("""
                SELECT visit_id, student_id, student_visit_reason, ta_id, enqueue_time, session_start FROM visits
                WHERE session_end IS NULL
            """).fetchall()

        visits = []
        for row in result:
            visits.append({
                "visit_id": row[0],
                "student_id": row[1],
                "student_visit_reason": row[2],
                "ta_id": row[3],
                "enqueue_time": row[4],
                "session_start": row[5]
            })
        return visits



