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
            "swipe_data": <string>
        }

    Returns:
        200 OK - Student was added to the queue
        404 Not Found - No student matching the card swipe was found
        {
            "message": <string>
        }
    """
    return f"{request.path} hit 😎, enqueue method is used"


@blueprint.route("/enqueue-ta-override", methods=["POST"])
def enqueue_ta_override():
    """
    role: TA

    Force enqueue a student.

    Resolving the id will be done in the order: UBIT -> pn -> id (Although, these _should_ all be unique so the order
    shouldn't matter)

    Args:
        body.identifier: A unique identifier for the student This can either be their UBIT, pn, or the id of their account

    Body:
        {
            "identifier": <string>
        }

    Returns:
        200 OK - Student was added to the queue
        403 Unauthorized - Requester does not have TA permissions
        404 Not Found - No student matching provided identifier
        {
            "message": <string>,
        }

    Use case: A student didn't bring their card to OH so they can't swipe in. The TA can force add them to the queue
    """
    return ""


@blueprint.route("/help-a-student", methods=["POST"])
def dequeue():
    """
    role: TA

    Remove the first student from the queue and create a Visit in the DB

    Not allowed if TA is already in a visit

    Returns:
        200 OK - Student was dequeued
        {
            "id": <int>,
            "username": <string>,
            "pn": <string>,
            "preferred_name: <string>
        }

        400 Bad Request - The queue is empty
        403 Unauthorized - Requester does not have TA permissions
        {
            "message": <string>
        }
    """
    return "Help them good!"


@blueprint.route("/get-queue", methods=["GET"])
def get_queue():
    """
    role: TA

    Returns all student accounts in the queue starting with the front of the queue

    Returns:
        200 OK
        [
            {
                "id": <int>,
                "username": <string>,
                "pn": <string>,
                "preferred_name: <string>
            },
            ...
        ]

        403 Unauthorized - Requester does not have TA permissions
        {
            "message": <string>
        }
    """
    return ""


@blueprint.route("/get-my-position", methods=["GET"])
def get_anon_queue():
    """
    role: self

    Returns the position in the queue of the requester. If the requester is not in the queue, return a position of -1

    Args:
        Request.cookie: The auth token used to identify the requester

    Returns:
        200 OK - You're in the queue and here's your position
        {
            "position": <int>
        }

        400 Bad Request - You are not in the queue
        {
            "message": <string>
        }
    """
    return ""


@blueprint.route("/remove-self-from-queue", methods=["POST"])
def remove_self():
    """
    role: self

    Remove the requester from the queue. Creates a visit in the db to store the reason for the removal

    Args:
        Request.cookie: The auth token used to identify the requester
        body.reason: a text reason for removing the user from the queue

    Body:
        {
            "reason": <string>
        }

    Returns:
        200 OK - You were removed from the queue and a visit was created
        400 Bad Request - You were not in the queue
        {
            "message": <string>
        }
    """
    return f"{request.path} hit 😎, remove method is used."


@blueprint.route("/remove-from-queue/<user_id>", methods=["POST"])
def remove(user_id):
    """
    role: TA

    Removing students from the queue by id. Creates a visit in the db to store the reason for the removal

    Args:
        param.user_id: The id of the student being removed. Note: This is the id of their account, not their UBIT/pn
        body.reason: a text reason for removing the user from the queue (eg. "No show")

    Body:
        {
            "reason": <string>
        }

    Returns:
        200 OK - Student was removed from the queue and a visit was created
        400 Bad Request - Student with user_id was not in the queue
        403 Unauthorized - Requester does not have TA permissions
        {
            "message": <string>
        }
    """
    return f"{request.path} hit 😎, remove method is used."
