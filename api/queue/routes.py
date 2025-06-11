"""Queue Blueprint for MOH"""

from flask import Blueprint, request

from api.database.db import db

blueprint = Blueprint("queue", __name__)


@blueprint.route("/enqueue-card-swipe", methods=["POST"])
def enqueue_card_swipe():
    """
    role: hardware

    Add student to the current live queue for office hours

    Args:
        body.swipe_data: The raw data from the card swipe as a string

    Body:
        {
            "swipe_data": "..."
        }

    Returns:
        A JSON of request status
        {
            "message": "You are enqueued",
        }
    """
    return f"{request.path} hit 😎, enqueue method is used"


@blueprint.route("/enqueue-ta-override", methods=["POST"])
def enqueue_ta_override():
    """
    role: TA

    Force enqueue a student into the queue.

    Resolving the id will be done in the order: UBIT -> pn -> id (Although, these _should_ all be unique so the order
    shouldn't matter)

    Args:
        body.id: A unique identifier for the student This can either be the id of their account, their pn, or their ubit

    Body:
        {
            "id": "..."
        }

    Use case: A student didn't bring their card to OH so they can't swipe in. The TA can force add them to the queue
    """
    pass
    return ""


@blueprint.route("/help-a-student", methods=["POST"])
def dequeue():
    """
    role: TA

    Remove the first student from the queue and create a Visit in the DB

    Not allowed if TA is already in a visit
    """
    return "Help them good!"


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


@blueprint.route("/remove-self-from-queue", methods=["POST"])
def remove_self():
    """Removing students from the queue based on id
    Args:
        Request.cookie: The auth token used to identify the requester
        body.reason: a text reason for removing the user from the queue. Will appear in the body of the request in a
                     json object

    Body:
        {
            "reason": "No show"
        }

    Returns:
        A JSON of request status
        {
            "message": "You are removed from the queue"
        }
    """
    return f"{request.path} hit 😎, remove method is used."


@blueprint.route("/remove-from-queue/<user_id>", methods=["POST"])
def remove(user_id):
    """Removing students from the queue by id
    Args:
        user_id: The id of the student being removed. Note: This is the id of their account, not their UBIT/pn
        body.reason: a text reason for removing the user from the queue. Will appear in the body of the request in a
                     json object

    Body:
        {
            "reason": "No show"
        }

    Returns:
        {
            "message": "You removed <user_id> from the queue"
        }
    """
    return f"{request.path} hit 😎, remove method is used."
