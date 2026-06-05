"""Visit management functions"""

from api.database.db import db


def get_students_visit(student):
    """Retrieves the in-progress visit involving the specified student, if it exists.

    :param student: the student's user id
    :return: the in-progress visit if it exists, None otherwise.
    """
    in_progress = db.get_in_progress_visits()
    in_progress = list(filter(lambda v: v["student_id"] == student, in_progress))

    if len(in_progress) == 0:
        return None

    visit = in_progress[0]
    ta = db.lookup_identifier(visit["ta_id"])

    return {"ta_name": ta["preferred_name"]}


def get_tas_visit(ta):
    """Retrieves the in-progress visit involving the specified TA, if it exists.

    :param ta: the TA's user id
    :return: the in-progress visit if it exists, None otherwise.
    """
    in_progress = db.get_in_progress_visits()
    in_progress = list(filter(lambda v: v["ta_id"] == ta, in_progress))

    if len(in_progress) == 0:
        return None

    visit = in_progress[0]
    student = db.lookup_identifier(visit["student_id"])

    return {
        "id": visit["student_id"],
        "username": student["ubit"],
        "pn": student["person_num"],
        "preferred_name": student["preferred_name"],
        "visitID": visit["visit_id"],
        "visit_reason": visit["student_visit_reason"],
    }
