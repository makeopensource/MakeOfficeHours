"""Queue Blueprint for MOH"""

from flask import Blueprint, request

blueprint = Blueprint("queue", __name__)


@blueprint.route("/enqueue-card-swipe", methods=["POST"])
def enqueue_card_swipe():
    """
    Add student to the current live queue for office hours

    Args:
        Request.cookie: A HTTP Cookie with the name `id` for the student being added.
        Cookie Example -
            "id": "12344567890" # only one field seems weird maybe more?

    Returns:
        A JSON of request status and possible wait time in seconds
        {
            "message": "You are enqueued",
            "wait_time": "5000"
        }
    """
    return f"{request.path} hit 😎, enqueue method is used"


@blueprint.route("/enqueue-ta-override", methods=["POST"])
def enqueue_ta_override():
    """
    Force enqueue a student into the queue. Only usable by TAs and instructors

    Use case: A student didn't bring their card to OH so they can't swipe in. The TA can force add them to the queue
    """
    return ""


@blueprint.route("/dequeue", methods=["DELETE"])
def dequeue():
    """
    Remove the first student from the queue and create a Visit in the DB
    """
    return ""


@blueprint.route("/get-queue", methods=["GET"])
def get_queue():
    """
    Returns all information about the queue. Only accessible by TAs and instructors
    """
    return ""


@blueprint.route("/get-anonymous-queue", methods=["GET"])
def get_anon_queue():
    """
    Returns the queue with all private information hidden. Only preferred names are displayed (Or no name for
    students who did not enter a preferred name)

    Contains time estimates. This can predict based on tags for the question (eg. a "task 5" tag might have
    a higher estimate than a "lecture question" tag)
    """
    return ""


@blueprint.route("/remove", methods=["DELETE"])
def remove():
    """Removing students from the queue based on id
    Args:
        Request.cookie: A HTTP Cookie with the name `id` for the student bring removed.
        Cookie Example -
            "id": "12344567890"

    Returns:
        A JSON of request status
        {
            "message": "You are removed from the queue"
        }
    """
    return f"{request.path} hit 😎, remove method is used."
