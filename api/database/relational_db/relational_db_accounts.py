import hashlib
import secrets

from api.database.idb_accounts import IAccounts
import bcrypt
import hashlib

from api.database.idb_roster import IRoster


class RelationalDBAccounts(IAccounts, IRoster):

    def create_account(self, ubit, pn):

        with self.cursor() as cursor:

            user_id = cursor.execute(
                """
                SELECT user_id FROM users WHERE ubit=? or person_num=?
            """,
                (ubit, pn),
            ).fetchone()

            if user_id is None:
                user_id = cursor.execute(
                    """
                    INSERT into users (ubit, person_num, course_role) VALUES (
                        ?, ?, "student"
                    )
                    RETURNING user_id; 
                """,
                    (ubit, pn),
                ).fetchone()[0]
            else:
                user_id = user_id[0]

        return user_id

    def lookup_person_number(self, person_number):

        with self.cursor() as cursor:
            user = cursor.execute(
                """
                SELECT preferred_name, last_name, ubit, person_num, course_role, user_id from users
                WHERE person_num = ?
            """,
                (person_number,),
            ).fetchone()

        if user is None:
            return None

        return {
            "preferred_name": user[0],
            "last_name": user[1],
            "ubit": user[2],
            "person_num": user[3],
            "course_role": user[4],
            "user_id": user[5],
        }

    def lookup_identifier(self, identifier):
        with self.cursor() as cursor:
            user = cursor.execute(
                """
                SELECT preferred_name, last_name, ubit, person_num, course_role, user_id from users
                WHERE ubit = ? OR person_num = ? OR user_id = ?
            """,
                (identifier, identifier, identifier),
            ).fetchone()

        if user is None:
            return None

        return {
            "preferred_name": user[0],
            "last_name": user[1],
            "ubit": user[2],
            "person_num": user[3],
            "course_role": user[4],
            "user_id": user[5],
        }

    def get_authenticated_user(self, auth_token):
        hashed_token = hashlib.sha256(auth_token.encode()).digest()
        with self.cursor() as cursor:
            user = cursor.execute(
                """
                SELECT preferred_name, last_name, ubit, person_num, course_role, users.user_id 
                FROM users
                INNER JOIN auth ON users.user_id = auth.user_id
                WHERE auth_token = ?
                AND expires_at > CURRENT_TIMESTAMP
            """,
                (hashed_token,),
            ).fetchone()

        if not user:
            return None

        return {
            "preferred_name": user[0],
            "last_name": user[1],
            "ubit": user[2],
            "person_num": user[3],
            "course_role": user[4],
            "user_id": user[5],
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

    def add_to_roster(self, user_id, role):

        with self.cursor() as cursor:
            cursor.execute(
                """
                UPDATE users
                SET course_role = ?
                WHERE user_id = ?
                """,
                (role, user_id),
            )

    def get_roster(self):
        with self.cursor() as cursor:
            users = cursor.execute("""
                SELECT user_id, preferred_name, last_name, ubit, person_num, course_role FROM users
                ORDER BY ubit
               """).fetchall()
            result = []
            for user in users:
                result.append({
                    "user_id": user[0],
                    "preferred_name": user[1],
                    "last_name": user[2],
                    "ubit": user[3],
                    "person_num": user[4],
                    "course_role": user[5]
                })

            return result


    def set_preferred_name(self, identifier, name):
        with self.cursor() as cursor:

            user = cursor.execute(
                """
                    UPDATE users SET preferred_name = ?
                    WHERE ubit = ? OR person_num = ? OR user_id = ?
                    RETURNING user_id
                """, (name, identifier, identifier, identifier)).fetchone()

            if user is None:
                return None

            return user[0]

    def set_name(self, user_id, first_name, last_name):
        with self.cursor() as cursor:
            user = cursor.execute(
                """
                    UPDATE users SET 
                    preferred_name = ?, last_name = ?
                    WHERE user_id = ?
                    RETURNING user_id
                """, (first_name, last_name, user_id)
            ).fetchone()

            if user is None:
                return None

            return user[0]