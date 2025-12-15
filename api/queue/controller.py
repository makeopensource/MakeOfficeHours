from api.database.db import db
from hardware.card_swipe import decode_pn


def add_to_queue_by_card_swipe(swipe_data):
    pn = decode_pn(swipe_data)
    student = db.lookup_person_number(pn)
    if student is not None:
        add_to_queue(student)
        return True
    return False


def add_to_queue_by_ta_override(identifier):
    student = db.lookup_identifier(identifier)
    if student is not None:
        add_to_queue(student)
        return True
    return False


def add_to_queue(user_account):
    user_id = user_account["user_id"]
    db.enqueue_student(user_id)
