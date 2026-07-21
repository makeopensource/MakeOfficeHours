"""Definition of the class containing session implementations"""

from api.database.idb_sessions import ISessions


class RelationalDBSessions(ISessions):
    """Implementations for the sessions component for the relational DB"""

    def update_swipe_time(self, user, course):
        with self.cursor() as cursor:
            cursor.execute(
                """
                UPDATE enrollments
                SET last_swipe = datetime('now', 'localtime')
                WHERE user_id = ? AND course_id = ?
            """,
                (user, course),
            )

    def reset_swipe_time(self, user, course):
        with self.cursor() as cursor:
            cursor.execute(
                """
                UPDATE enrollments
                SET last_swipe = NULL
                WHERE user_id = ? AND course_id = ?
            """,
                (user, course),
            )

    def get_swipe_time(self, user, course):
        with self.cursor() as cursor:
            time = cursor.execute(
                """
                SELECT last_swipe FROM enrollments 
                WHERE last_swipe > datetime('now', 'localtime', '-2 hours') 
                  AND user_id = ? AND course_id = ?
            """,
                (user, course),
            ).fetchone()

        if time is None:
            return None

        return time[0]

    def get_on_site(self, course):
        with self.cursor() as cursor:
            users = cursor.execute(
                """
                SELECT users.user_id, preferred_name, ubit, person_num
                FROM users
                         LEFT JOIN queue ON users.user_id = queue.user_id
                        INNER JOIN enrollments as e on users.user_id = e.user_id
                WHERE last_swipe > datetime('now', 'localtime', '-2 hours')
                  AND queue.user_id IS NULL AND e.course_id = ?
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

    def clear_on_site(self, course):
        with self.cursor() as cursor:
            cursor.execute(
                """
                UPDATE enrollments SET last_swipe = NULL WHERE course_id = ?
            """,
                (course,),
            )
