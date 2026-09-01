""" Courses methods for SQLite implementation """
from api.database.idb_courses import ICourses

class RelationalDBCourses(ICourses):
    """ Class implementing the respective courses methods """

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
