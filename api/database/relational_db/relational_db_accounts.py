from api.database.idb_accounts import IAccounts

class RelationalDBAccounts(IAccounts):

    def create_account(self, ubit, pn):

        user_id = self.cursor.execute('''
            SELECT user_id FROM users WHERE ubit=? or person_num=?
        ''', (ubit, pn)).fetchone()

        if user_id is None:
            user_id = self.cursor.execute('''
                INSERT into users (ubit, person_num, course_role) VALUES (
                    ?, ?, "student"
                )
                RETURNING user_id; 
            ''', (ubit, pn)).fetchone()[0]
            self.connection.commit()
        else:
            user_id = user_id[0]

        return user_id

    def lookup_person_number(self, person_number):
        user = self.cursor.execute('''
            SELECT preferred_name, last_name, ubit, person_num, course_role, user_id from users
            WHERE person_num = ?
        ''', (person_number,)).fetchone()

        if user is None:
            return None

        return {
            "preferred_name": user[0],
            "last_name": user[1],
            "ubit": user[2],
            "person_num": user[3],
            "course_role": user[4],
            "user_id": user[5]
        }

    def lookup_identifier(self, identifier):
        user = self.cursor.execute('''
            SELECT preferred_name, last_name, ubit, person_num, course_role, user_id from users
            WHERE ubit = ? OR person_num = ? OR user_id = ?
        ''', (identifier, identifier, identifier)).fetchone()

        if user is None:
            return None

        return {
            "preferred_name": user[0],
            "last_name": user[1],
            "ubit": user[2],
            "person_num": user[3],
            "course_role": user[4],
            "user_id": user[5]
        }