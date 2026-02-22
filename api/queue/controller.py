import datetime

from api.database.db import db


def decode_pn(raw):
    try:
        return raw.split("/^")[1][14:22]
    except Exception:
        return ""


def add_to_queue_by_card_swipe(swipe_data):
    pn = decode_pn(swipe_data)
    student = db.lookup_person_number(pn)
    if student is not None:
        add_to_queue(student)
        db.update_swipe_time(student["user_id"])
        return True
    return False


def add_to_queue_by_ta_override(identifier, front=False):
    student = db.lookup_identifier(identifier)
    if student is not None:
        if front:
            add_to_front_of_queue(student)
        else:
            add_to_queue(student)
        db.update_swipe_time(student["user_id"])
        return True
    return False


def add_to_queue(user_account):
    user_id = user_account["user_id"]
    db.enqueue_student(user_id)

def add_to_front_of_queue(user_account):
    user_id = user_account["user_id"]
    db.enqueue_student_front(user_id)

def remove_from_queue_without_visit(student, reason):
    queue_info = db.remove_student(student)

    if queue_info is None:
        return False

    visit = db.create_visit(student, None, queue_info["joined"], "")
    db.end_visit(visit, reason)
    return True

def self_add_to_queue(student):
    if is_active(student):
        db.enqueue_student(student)
        return True
    return False

def is_active(student):
    # YYYY-MM-DD HH:MM:SS
    time_format = "%Y-%m-%d %H:%M:%S"

    now = datetime.datetime.now()
    enqueue_time = db.get_swipe_time(student)

    if enqueue_time is None:
        return False

    enqueue_time = datetime.datetime.strptime(enqueue_time, time_format)

    seconds = (now - enqueue_time).seconds

    if seconds > 7200:
        return False

    return True

def get_students_visit(student):
    in_progress = db.get_in_progress_visits()
    in_progress = list(filter(lambda v: v["student_id"] == student, in_progress))

    if len(in_progress) == 0:
        return None


    visit = in_progress[0]
    ta = db.lookup_identifier(visit["ta_id"])

    return {
        "ta_name": ta["preferred_name"]
    }


def get_tas_visit(ta):

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
        "visit_reason": visit["student_visit_reason"]
    }



