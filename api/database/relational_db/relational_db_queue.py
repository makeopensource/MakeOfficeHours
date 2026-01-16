import datetime

from api.database.idb_queue import IQueue


class RelationalDBQueue(IQueue):

    def enqueue_student(self, student):
        with self.cursor() as cursor:
            cursor.execute(
                """
                INSERT OR IGNORE INTO queue (user_id, priority) VALUES (?, 0)
            """,
                (student,),
            )

    def enqueue_student_front(self, student):
        with self.cursor() as cursor:
            priority = cursor.execute("SELECT MAX(priority) FROM queue").fetchone()[0]
            if priority is None:
                priority = 0
            else:
                priority += 1

            cursor.execute(
                """
                INSERT OR IGNORE INTO queue (user_id, priority)
                VALUES (?, ?)
                """,
                (student, priority),
            )

    def dequeue_student(self):
        with self.cursor() as cursor:
            rows = cursor.execute("SELECT COUNT(*) from queue").fetchone()[0]
            if rows == 0:
                return None

            user = cursor.execute(
                """
                SELECT users.user_id, preferred_name, ubit, person_num, joined 
                FROM queue 
                INNER JOIN users ON queue.user_id = users.user_id 
                ORDER BY priority DESC, joined
            """
            ).fetchone()
            cursor.execute("DELETE FROM queue WHERE user_id = ?", (user[0],))

        return {
            "user_id": user[0],
            "preferred_name": user[1],
            "ubit": user[2],
            "person_num": str(user[3]),
            "enqueue_time": user[4]
        }

    def dequeue_specified_student(self, student_id):
        with self.cursor() as cursor:
            user = cursor.execute(
                """
                SELECT users.user_id, preferred_name, ubit, person_num, joined, enqueue_reason 
                FROM queue 
                INNER JOIN users ON queue.user_id = users.user_id 
                WHERE users.user_id = ?
            """, (student_id,)
            ).fetchone()

            if user is None:
                return None

            cursor.execute("DELETE FROM queue WHERE user_id = ?", (user[0],))

        return {
            "user_id": user[0],
            "preferred_name": user[1],
            "ubit": user[2],
            "person_num": str(user[3]),
            "enqueue_time": user[4],
            "enqueue_reason": user[5]
        }

    def get_queue(self):
        with self.cursor() as cursor:
            users = cursor.execute(
                "SELECT users.user_id, preferred_name, ubit, person_num FROM queue INNER JOIN users ON queue.user_id = users.user_id ORDER BY joined"
            )

            users_l = list()

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

    def clear_queue(self):
        with self.cursor() as cursor:
            cursor.execute(
                "DELETE FROM queue"
            )

    def remove_student(self, student):
        with self.cursor() as cursor:
            queue_info = cursor.execute("SELECT * FROM queue WHERE user_id = ?", (student, )).fetchone()

            if queue_info is None:
                return None

            cursor.execute("DELETE FROM queue WHERE user_id = ?", (student, ))

            return {"user_id": queue_info[0], "joined": queue_info[1]}

    def set_reason(self, student, reason):
        with self.cursor() as cursor:
            cursor.execute(
                "UPDATE queue SET enqueue_reason = ? WHERE user_id = ?", (reason, student)
            )

    def move_to_end(self, student):
        now = str(datetime.datetime.now().isoformat(' ', timespec="seconds"))

        with self.cursor() as cursor:
            cursor.execute(
                "UPDATE queue SET joined = ?, priority = 0 WHERE user_id = ?", (now, student)
            )