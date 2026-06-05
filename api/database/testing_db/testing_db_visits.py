"""Visits and Sessions part of the testing DB"""

from api.database.idb_sessions import ISessions
from api.database.idb_visits import IVisits


class TestingDBVisits(IVisits, ISessions):
    """Visit and session implementation for testing DB"""

    def create_visit(self, student, ta, enqueue_time, visit_reason) -> int:
        pass

    def end_visit(self, visit_id, reason):
        pass

    def cancel_visit(self, visit_id):
        pass

    def get_in_progress_visits(self):
        pass

    def get_visits(self, user_id=None):
        pass

    def update_swipe_time(self, user):
        pass

    def reset_swipe_time(self, user):
        pass

    def get_swipe_time(self, user):
        pass

    def get_on_site(self):
        pass

    def clear_on_site(self):
        pass
