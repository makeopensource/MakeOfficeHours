"""Queue component for the relational DB"""

import datetime
import secrets

from api.database.idb_queue import IQueue


class RelationalDBQueue(IQueue):
    """Implementations of the database queue methods."""

    def enqueue_student(self, student, course):
        with self.cursor() as cursor:
            cursor.execute(
                """
                INSERT OR IGNORE INTO queue (user_id, priority, course_id) VALUES (?, 0, ?)
            """,
                (student, course),
            )

    def enqueue_student_front(self, student, course):
        with self.cursor() as cursor:
            priority = cursor.execute(
                "SELECT MAX(priority) FROM queue WHERE course_id = ?", (course,)
            ).fetchone()[0]
            if priority is None:
                priority = 0
            else:
                priority += 1

            cursor.execute(
                """
                INSERT OR IGNORE INTO queue (user_id, priority, course_id)
                VALUES (?, ?, ?)
                """,
                (student, priority, course),
            )

    def dequeue_student(self, course):
        with self.cursor() as cursor:
            rows = cursor.execute("SELECT COUNT(*) from queue").fetchone()[0]
            if rows == 0:
                return None

            user = cursor.execute(
                """
                SELECT users.user_id, preferred_name, ubit, person_num, joined 
                FROM queue
                INNER JOIN users ON queue.user_id = users.user_id 
                WHERE course_id = ?
                ORDER BY priority DESC, joined
            """,
                (course,),
            ).fetchone()
            cursor.execute(
                "UPDATE queue SET dequeued = true WHERE user_id = ?", (user[0],)
            )

        return {
            "user_id": user[0],
            "preferred_name": user[1],
            "ubit": user[2],
            "person_num": str(user[3]),
            "enqueue_time": user[4],
        }

    def dequeue_specified_student(self, student_id, course):
        with self.cursor() as cursor:
            user = cursor.execute(
                """
                SELECT users.user_id, preferred_name, ubit, person_num, joined, enqueue_reason 
                FROM queue 
                INNER JOIN users ON queue.user_id = users.user_id 
                WHERE users.user_id = ? AND course_id = ?
            """,
                (student_id, course),
            ).fetchone()

            if user is None:
                return None

            cursor.execute(
                "UPDATE queue SET dequeued = true WHERE user_id = ?", (user[0],)
            )

        return {
            "user_id": user[0],
            "preferred_name": user[1],
            "ubit": user[2],
            "person_num": str(user[3]),
            "enqueue_time": user[4],
            "enqueue_reason": user[5],
        }

    def get_queue(self, course):
        with self.cursor() as cursor:
            users = cursor.execute(
                """
                SELECT users.user_id, preferred_name, ubit, person_num 
                FROM queue INNER JOIN users ON queue.user_id = users.user_id 
                WHERE dequeued = false AND course_id = ?
                ORDER BY priority DESC, joined
                """,
                (course,),
            )

            users_l = []

            for user in users:
                users_l.append(
                    {
                        "id": user[0],
                        "preferred_name": user[1],
                        "ubit": user[2],
                        "pn": user[3],
                    }
                )

        return users_l

    def clear_queue(self, course):
        with self.cursor() as cursor:
            cursor.execute(
                "DELETE FROM queue WHERE dequeued = false AND course_id = ?", (course,)
            )

    def remove_student(self, student, course):
        with self.cursor() as cursor:
            queue_info = cursor.execute(
                "SELECT * FROM queue WHERE user_id = ? AND course_id = ?",
                (student, course),
            ).fetchone()

            if queue_info is None:
                return None

        with self.cursor() as cursor:
            cursor.execute(
                "DELETE FROM queue WHERE user_id = ? AND course_id = ?",
                (student, course),
            )

            return {"user_id": queue_info[0], "joined": queue_info[1]}

    def set_reason(self, student, reason, course):
        with self.cursor() as cursor:
            cursor.execute(
                "UPDATE queue SET enqueue_reason = ? WHERE user_id = ? AND course_id = ?",
                (reason, student, course),
            )

    def move_to_end(self, student, course):
        now = str(datetime.datetime.now().isoformat(" ", timespec="seconds"))

        with self.cursor() as cursor:
            res = cursor.execute(
                "UPDATE queue SET joined = ?, priority = 0 WHERE user_id = ? AND course_id = ? RETURNING user_id",
                (now, student, course),
            ).fetchone()
            if res is None:
                return False
            return True

    def get_hw_authorization(self, course):
        with self.cursor() as cursor:
            res = cursor.execute(
                "SELECT authorization FROM hardware WHERE expires_at > CURRENT_TIMESTAMP AND course_id = ?",
                (course,),
            ).fetchone()

            if res is None:
                return res

            return res[0]

    def reset_hw_authorization(self, course):
        with self.cursor() as cursor:
            cursor.execute("DELETE FROM hardware")

            auth_code = secrets.token_urlsafe(16)

            cursor.execute(
                "INSERT INTO hardware (authorization, course_id) VALUES (?, ?)",
                (auth_code, course),
            )

            return auth_code
