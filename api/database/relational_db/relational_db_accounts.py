import secrets

from api.database.idb_accounts import IAccounts
import bcrypt


class RelationalDBAccounts(IAccounts):

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
        with self.cursor() as cursor:
            user = cursor.execute(
                """
                SELECT preferred_name, last_name, ubit, person_num, course_role, users.user_id 
                FROM users
                INNER JOIN auth ON users.user_id = auth.user_id
                WHERE auth_token = ?
                AND expires_at > CURRENT_TIMESTAMP
            """,
                (auth_token,),
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
                (hashed, auth, username),
            ).fetchone()


        if not auth_token:
            return None

        return auth_token[0]

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

        with self.cursor() as cursor:
            cursor.execute(
                """
                UPDATE auth
                SET auth_token = ?, expires_at = datetime('now', '+30 days')
                WHERE user_id = ?
            """,
                (auth_token, user_id),
            )

        return auth_token

    def sign_out(self, auth_token):
        with self.cursor() as cursor:
            cursor.execute(
                """
            UPDATE auth
            SET auth_token = "", expires_at = CURRENT_TIMESTAMP
            WHERE auth_token = ?
            """,
                (auth_token,),
            )
