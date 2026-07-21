"""Accounts and roster methods for SQLite implementation"""

import datetime
import secrets
import hashlib

import bcrypt

from api.database.idb_accounts import IAccounts
from api.database.idb_courses import ICourses
from api.database.idb_roster import IRoster


class RelationalDBAccounts(IAccounts, IRoster, ICourses):
    """Implementations for the accounts and roster components."""

    def get_courses(self) -> list[dict[str, str]]:
        with self.cursor() as cursor:
            courses = cursor.execute(
                """
                SELECT course_id, course_name, course_sem, course_url FROM courses 
            """
            ).fetchall()

            courses_l = []

            for course in courses:
                courses_l.append(dict(course))

        return courses_l

    def get_enrollments(self, user_id):
        with self.cursor() as cursor:
            courses = cursor.execute(
                """
                SELECT c.course_id, course_name, course_sem, course_url, course_role FROM courses as c 
                INNER JOIN enrollments as e 
                ON c.course_id = e.course_id
                WHERE e.user_id = ?
            """,
                (user_id,),
            ).fetchall()

            courses_l = []
            for course in courses:
                courses_l.append(dict(course))

        return courses_l

    def create_course(self, name, semester, url) -> int:
        with self.cursor() as cursor:
            prev = cursor.execute(
                "SELECT * FROM courses WHERE course_url = ? OR course_id = ?",
                (url, url),
            ).fetchone()
            if prev is not None:
                return -1

            course = cursor.execute(
                "INSERT INTO courses (course_name, course_sem, course_url) VALUES (?, ?, ?) RETURNING *",
                (name, semester, url),
            ).fetchone()

            return course["course_id"]

    def get_course(self, identifier) -> dict[str, str]:
        with self.cursor() as cursor:
            result = cursor.execute(
                "SELECT * FROM courses WHERE course_id = ? OR course_url = ?",
                (identifier, identifier),
            ).fetchone()
            return dict(result) if result is not None else None

    def create_account(self, ubit, pn):

        with self.cursor() as cursor:

            user_id = cursor.execute(
                """
                SELECT user_id FROM users WHERE (ubit=? or person_num=?)
            """,
                (ubit, pn),
            ).fetchone()

            if user_id is None:
                user_id = cursor.execute(
                    """
                    INSERT into users (ubit, person_num, site_role) VALUES (
                        ?, ?, 'user'
                    )
                    RETURNING user_id; 
                """,
                    (ubit, pn),
                ).fetchone()[0]
            else:
                user_id = user_id[0]

        return user_id

    def _get_course_role(self, user_id, course):

        if course is None:
            return None

        course = self.get_course(course)

        with self.cursor() as cursor:
            role = cursor.execute(
                "SELECT course_role FROM enrollments WHERE user_id = ? AND course_id = ?",
                (
                    user_id,
                    course["course_id"],
                ),
            ).fetchone()
        if role is not None:
            return role["course_role"]
        return None

    def lookup_person_number(self, person_number, course=None):

        with self.cursor() as cursor:
            user = cursor.execute(
                """
                SELECT preferred_name, last_name, ubit, person_num, site_role, user_id from users

                WHERE person_num = ?
            """,
                (person_number,),
            ).fetchone()
            if user is None:
                return None

        course_role = self._get_course_role(user["user_id"], course)

        return {
            "preferred_name": user[0],
            "last_name": user[1],
            "ubit": user[2],
            "person_num": user[3],
            "site_role": user[4],
            "user_id": user[5],
            "course_role": course_role,
        }

    def lookup_identifier(self, identifier, course=None):
        with self.cursor() as cursor:
            user = cursor.execute(
                """
                SELECT preferred_name, last_name, ubit, person_num, site_role, user_id from users
                WHERE (ubit = ? OR person_num = ? OR user_id = ?)
            """,
                (identifier, identifier, identifier),
            ).fetchone()

            if not user:
                return None

            course_role = self._get_course_role(user["user_id"], course)

            return {
                "preferred_name": user["preferred_name"],
                "last_name": user["last_name"],
                "ubit": user["ubit"],
                "person_num": user["person_num"],
                "site_role": user["site_role"],
                "user_id": user["user_id"],
                "course_role": course_role,
            }

    def get_authenticated_user(self, auth_token, course=None):
        hashed_token = hashlib.sha256(auth_token.encode()).digest()
        with self.cursor() as cursor:
            user = cursor.execute(
                """
                SELECT preferred_name, last_name, ubit, person_num, site_role, users.user_id 
                FROM users
                INNER JOIN auth ON users.user_id = auth.user_id
                WHERE auth_token = ? 
                AND expires_at > CURRENT_TIMESTAMP
            """,
                (hashed_token,),
            ).fetchone()

        if not user:
            return None

        # TODO: fix this
        enqueue_time = None

        if enqueue_time is None:
            on_site = False
        else:
            # YYYY-MM-DD HH:MM:SS
            time_format = "%Y-%m-%d %H:%M:%S"

            now = datetime.datetime.now()
            enqueue_time = datetime.datetime.strptime(enqueue_time, time_format)
            seconds = (now - enqueue_time).seconds

            on_site = seconds <= 7200

        return {
            "preferred_name": user[0],
            "last_name": user[1],
            "ubit": user[2],
            "person_num": user[3],
            "site_role": user[4],
            "user_id": user[5],
            "on_site": on_site,
            "course_role": self._get_course_role(user["user_id"], course),
        }

    def sign_up(self, username, pw) -> str | None:

        hashed = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
        auth = secrets.token_urlsafe(32)
        hashed_auth = hashlib.sha256(auth.encode()).digest()

        with self.cursor() as cursor:
            auth_token = cursor.execute(
                """
                INSERT OR IGNORE 
                INTO auth (user_id, pw, auth_token)
                SELECT user_id, ?, ?
                FROM users
                WHERE users.ubit = ?
                RETURNING auth_token
            """,
                (hashed, hashed_auth, username),
            ).fetchone()

        if not auth_token:
            return None

        return auth

    def _generate_auth_token(self, user_id):
        auth_token = secrets.token_urlsafe(32)
        hashed_auth = hashlib.sha256(auth_token.encode()).digest()

        with self.cursor() as cursor:
            cursor.execute(
                """
                UPDATE auth
                SET auth_token = ?, expires_at = datetime('now', '+30 days')
                WHERE user_id = ?
            """,
                (hashed_auth, user_id),
            )

        return auth_token

    def sign_in(self, username, pw) -> str | None:
        with self.cursor() as cursor:
            hashed = cursor.execute(
                """
                SELECT users.user_id, pw FROM auth 
                INNER JOIN users on users.user_id = auth.user_id
                WHERE users.ubit = ?
            """,
                (username,),
            ).fetchone()

        if not hashed:
            return None

        user_id = hashed[0]
        hashed = hashed[1]
        if not bcrypt.checkpw(pw.encode(), hashed):
            return None

        auth_token = self._generate_auth_token(user_id)
        return auth_token

    def sign_in_with_autolab(self, ubit) -> str | None:
        with self.cursor() as cursor:
            cursor.execute(
                """
                INSERT OR IGNORE 
                INTO auth (user_id)
                VALUES (?)
            """,
                (ubit,),
            )

        auth_token = self._generate_auth_token(ubit)
        return auth_token

    def sign_out(self, auth_token):
        hashed_auth = hashlib.sha256(auth_token.encode()).digest()
        with self.cursor() as cursor:
            cursor.execute(
                """
            UPDATE auth
            SET auth_token = "", expires_at = CURRENT_TIMESTAMP
            WHERE auth_token = ?
            """,
                (hashed_auth,),
            )

    def add_to_roster(self, user_id, role, course):

        with self.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO enrollments (course_id, user_id, course_role) VALUES (?, ?, ?)
                """,
                (course, user_id, role),
            )

    def get_roster(self, course):
        with self.cursor() as cursor:
            users = cursor.execute(
                """
                SELECT users.user_id, preferred_name, last_name, ubit, person_num, site_role, e.course_role FROM users
                INNER JOIN enrollments as e ON e.user_id = users.user_id
                WHERE course_id = ?
                ORDER BY ubit
               """,
                (course,),
            ).fetchall()
            result = []
            for user in users:
                result.append(
                    {
                        "user_id": user[0],
                        "preferred_name": user[1],
                        "last_name": user[2],
                        "ubit": user[3],
                        "person_num": user[4],
                        "site_role": user[5],
                        "course_role": user[6],
                    }
                )

            return result

    def set_preferred_name(self, identifier, name):
        with self.cursor() as cursor:

            user = cursor.execute(
                """
                    UPDATE users SET preferred_name = ?
                    WHERE ubit = ? OR person_num = ? OR user_id = ?
                    RETURNING user_id
                """,
                (name, identifier, identifier, identifier),
            ).fetchone()

            if user is None:
                return None

            return user[0]

    def set_initial_name(self, user_id, first_name, last_name):
        with self.cursor() as cursor:
            user = cursor.execute(
                """
                    UPDATE users SET 
                    preferred_name = ?, last_name = ?
                    WHERE user_id = ? AND preferred_name IS NULL
                    RETURNING user_id
                """,
                (first_name, last_name, user_id),
            ).fetchone()

            if user is None:
                return None

            return user[0]

    def remove_from_roster(self, user_id, course):
        with self.cursor() as cursor:
            user = cursor.execute(
                """
                    DELETE FROM enrollments
                    WHERE user_id = ? AND course_id = ?
                    RETURNING user_id
                """,
                (user_id, course),
            ).fetchone()

            if user is None:
                return None

        return user["user_id"]

    def delete_user(self, user_id):
        with self.cursor() as cursor:
            user = cursor.execute(
                """
                    UPDATE users SET deleted = true
                    WHERE user_id = ?
                    RETURNING user_id
                """,
                (user_id,),
            ).fetchone()

            if user is None:
                return None

        return user[0]

    def clear_students(self, course):
        with self.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM enrollments WHERE course_role = 'student' AND course_id = ?
            """,
                (course,),
            )
