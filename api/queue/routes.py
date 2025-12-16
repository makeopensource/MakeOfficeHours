"""Queue Blueprint for MOH"""

from flask import Blueprint, request

import api.queue.controller as controller
from api.roster.controller import permission_required
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

    body = request.get_json()
    swipe_data = body["swipe_data"]

    if controller.add_to_queue_by_card_swipe(swipe_data):
        return {"message": "Student was added to the queue"}

    return {"message": "No student matching the card swipe was found"}, 404


@blueprint.route("/enqueue-ta-override", methods=["POST"])
@permission_required("ta")
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

    body = request.get_json()
    identifier = body["identifier"]

    if controller.add_to_queue_by_ta_override(identifier):
        return {"message": "Student was added to the queue"}

    return {"message": "No student matching provided identifier"}, 404


@blueprint.route("/help-a-student", methods=["POST"])
@permission_required("ta")
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

    student = db.dequeue_student()

    if student is None:
        return {"message": "The queue is empty"}, 400

    return {
        "id": int(student["user_id"]),
        "username": student["ubit"],
        "pn": str(student["person_num"]),
        "preferred_name": student["preferred_name"],
    }


@blueprint.route("/get-queue", methods=["GET"])
@permission_required("ta")
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

    # todo: permission checking. needs auth.

    return db.get_queue()


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
    if not (auth_token := request.cookies.get("auth_token")):
        return {"message": "You are not logged in!"}, 403

    user = db.get_authenticated_user(auth_token)

    if not user:
        return {"message": "You are not logged in!"}, 403

    user_id = user["user_id"]

    queue = db.get_queue()

    for i, entry in enumerate(queue, 1):
        if entry["id"] == user_id:
            return {"position": i}

    return {"message": "You are not in the queue!"}, 400


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


@blueprint.route("/remove-from-queue", methods=["POST"])
def remove(user_id):
    """
    role: TA

    Removing students from the queue by id. Creates a visit in the db to store the reason for the removal

    Args:
        param.user_id: The id of the student being removed. Note: This is the id of their account, not their UBIT/pn
        body.reason: a text reason for removing the user from the queue (eg. "No show")
        body.user_id: user ID of the student being removed

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


# TODO: move to end of queue (Called by TAs to add the students they just saw back to the end of the queue)

# TODO: Clear the queue
