from api.database.idb_queue import IQueue


class RelationalDBQueue(IQueue):

    def enqueue_student(self, student):
        with self.cursor() as cursor:
            cursor.execute(
                """
                INSERT OR IGNORE INTO queue (user_id) VALUES (?)
            """,
                (student,),
            )

    def dequeue_student(self):
        with self.cursor() as cursor:
            rows = cursor.execute("SELECT COUNT(*) from queue").fetchone()[0]
            if rows == 0:
                return None

            user = cursor.execute(
                """
                SELECT users.user_id, preferred_name, ubit, person_num 
                FROM queue 
                INNER JOIN users ON queue.user_id = users.user_id 
                ORDER BY joined
            """
            ).fetchone()
            cursor.execute("DELETE FROM queue WHERE user_id = ?", (user[0],))

        return {
            "user_id": user[0],
            "preferred_name": user[1],
            "ubit": user[2],
            "person_num": str(user[3]),
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
