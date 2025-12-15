from api.database.idb_queue import IQueue


class RelationalDBQueue(IQueue):

    def enqueue_student(self, student):
        self.cursor.execute(
            """
            INSERT OR IGNORE INTO queue (user_id) VALUES (?)
        """,
            (student,),
        )

        self.connection.commit()

    def dequeue_student(self):
        rows = self.cursor.execute("SELECT COUNT(*) from queue").fetchone()[0]
        if rows == 0:
            return None

        user = self.cursor.execute(
            """
            SELECT users.user_id, preferred_name, ubit, person_num 
            FROM queue 
            INNER JOIN users ON queue.user_id = users.user_id 
            ORDER BY joined
        """
        ).fetchone()
        self.cursor.execute("DELETE FROM queue WHERE user_id = ?", (user[0],))

        self.connection.commit()

        return {
            "user_id": user[0],
            "preferred_name": user[1],
            "ubit": user[2],
            "person_num": str(user[3]),
        }

    def get_queue(self):
        users = self.cursor.execute(
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
