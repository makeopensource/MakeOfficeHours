"""Visits and Sessions part of the testing DB"""

from api.database.idb_courses import ICourses
from api.database.idb_sessions import ISessions
from api.database.idb_visits import IVisits


class TestingDBVisits(IVisits, ISessions, ICourses):
    """Visit and session implementation for testing DB"""

    def create_course(self, name, semester, url) -> int:
        pass

    def get_course(self, identifier) -> dict[str, str]:
        pass

    def get_courses(self) -> list[dict[str, str]]:
        pass

    def create_visit(self, student, ta, enqueue_time, visit_reason, course) -> int:
        pass

    def end_visit(self, visit_id, reason):
        pass

    def cancel_visit(self, visit_id):
        pass

    def get_in_progress_visits(self, course):
        pass

    def get_visits(self, course, user_id=None):
        pass

    def update_swipe_time(self, user, course):
        pass

    def reset_swipe_time(self, user, course):
        pass

    def get_swipe_time(self, user, course):
        pass

    def get_on_site(self, course):
        pass

    def clear_on_site(self, course):
        pass
