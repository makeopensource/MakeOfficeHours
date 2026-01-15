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
        return True
    return False


def add_to_queue_by_ta_override(identifier, front=False):
    student = db.lookup_identifier(identifier)
    if student is not None:
        if front:
            add_to_front_of_queue(student)
        else:
            add_to_queue(student)
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
    visit = db.create_visit(student, None, queue_info["joined"], "")
    db.end_visit(visit, reason)

