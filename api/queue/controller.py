"""Queue management functions"""

import datetime

from api.database.db import db


def decode_pn(raw):
    """Decode a person number from raw card swipe data, based on UB's card format.

    :param raw: the raw data from the card swipe

    :return: The parsed data on success, empty string on failure
    """
    try:
        return raw.split("/^")[1][14:22]
    except IndexError:
        return ""


def add_to_queue_by_card_swipe(swipe_data):
    """Parse the raw swipe data and enqueue user matching the person number.
    Should also reset the user's swipe time to the current timestamp.

    :param swipe_data: the raw swipe data

    :return True on success, False on failure
    """
    pn = decode_pn(swipe_data)
    student = db.lookup_person_number(pn)
    if student is not None:
        add_to_queue(student)
        db.update_swipe_time(student["user_id"])
        return True
    return False


def add_to_queue_by_ta_override(identifier, front=False):
    """Add the specified user to the queue.
    Should also reset the specified user's swipe time to the current timestamp.

    :param identifier: the user's identifier
    :param front: (optional) whether to add the user to the front or back of the queue
    :return: True on success, False on failure
    """
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
    """Adds the specified user to the back of the queue.

    :param user_account: a dict containing the user's id in a field named "user_id"
    """
    user_id = user_account["user_id"]
    db.enqueue_student(user_id)


def add_to_front_of_queue(user_account):
    """Adds the specified user to the front of the queue.

    :param user_account: a dict containing the user's id in a field named "user_id"
    """
    user_id = user_account["user_id"]
    db.enqueue_student_front(user_id)


def remove_from_queue_without_visit(student, reason):
    """Removes the specified student from the queue and immediately
    closes the visit for the specified reason.

    :param student: the user id of the student to remove
    :param reason: the reason for removal
    :return: True on success, False on failure
    """
    queue_info = db.remove_student(student)

    if queue_info is None:
        return False

    visit = db.create_visit(student, None, queue_info["joined"], "")
    db.end_visit(visit, reason)
    return True


def self_add_to_queue(student):
    """Attempt to add the specified student to the queue.
    Should fail if the user hasn't refreshed their swipe
    within the past two hours.

    :param student: The user id of the student to add
    :return: True on success, False on failure
    """
    if is_active(student):
        db.enqueue_student(student)
        return True
    return False


def is_active(student):
    """Checks if the student has refreshed their swipe
    within the past two hours.

    :param student: The user id of the student to check
    :return:        True if the user has refreshed within the past two hours,
                    False otherwise
    """
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
