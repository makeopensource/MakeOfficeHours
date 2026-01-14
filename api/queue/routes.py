"""Queue Blueprint for MOH"""

from flask import Blueprint, request

import api.queue.controller as controller
from api.queue.controller import remove_from_queue_without_visit
from api.roster.controller import min_level
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
@min_level("ta")
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
@min_level("ta")
def dequeue():
    """
    role: TA

    Remove the specified student from the queue and create a Visit in the DB

    Not allowed if TA is already in a visit

    Args:
        body.id: The ID of the account to dequeue

    Body:
        {
            "id": <string>
        }

    Returns:
        200 OK - Student was dequeued
        {
            "id": <int>,
            "username": <string>,
            "pn": <string>,
            "preferred_name: <string>
        }

        400 Bad Request - The queue is empty or user is not in the queue
        403 Unauthorized - Requester does not have TA permissions
        {
            "message": <string>
        }
    """

    body = request.get_json()

    if not (auth_token := request.cookies.get("auth_token")):
        return {"message": "You are not logged in!"}, 403

    user = db.get_authenticated_user(auth_token)
    user_id = user["user_id"]

    student = db.dequeue_specified_student(body["id"])

    if student is None:
        return {"message": "The queue is empty"}, 400

    visit = db.create_visit(body["id"], user_id, student["enqueue_time"])

    return {
        "id": int(student["user_id"]),
        "username": student["ubit"],
        "pn": str(student["person_num"]),
        "preferred_name": student["preferred_name"],
        "visitID": visit
    }


@blueprint.route("/get-queue", methods=["GET"])
@min_level("ta")
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

    Returns the position in the queue of the requester.

    Args:
        Request.cookie: The auth token used to identify the requester

    Returns:
        200 OK - You're in the queue and here's your position
        {
            "position": <int>,
            "length": <int>
        }

        400 Bad Request - You are not in the queue
        {
            "message": <string>,
            "length": <int>
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
            return {"position": i, "length": len(queue)}

    return {"message": "You are not in the queue!", "length": len(queue)}, 400


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

    if not (auth_token := request.cookies.get("auth_token")):
        return {"message": "You are not logged in!"}, 403

    user = db.get_authenticated_user(auth_token)

    if not user:
        return {"message": "You are not logged in!"}, 403

    user_id = user["user_id"]
    body = request.get_json()

    remove_from_queue_without_visit(user_id, f"[SELF-REMOVE]: {body["reason"]}")



    return {"message":"Removed self from queue."}


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

@blueprint.route("/clear-queue", methods=["DELETE"])
@min_level('ta')
def clear_queue():
    db.clear_queue()
    return {"message": "Successfully cleared the queue."}


@blueprint.route("/enqueue-override-front")
@min_level('ta')
def enqueue_override_front():
    """ Exact same behavior as /enqueue-ta-override, except it sends the student to the front.

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
    """
    body = request.get_json()
    identifier = body["identifier"]

    if controller.add_to_queue_by_ta_override(identifier, True):
        return {"message": "Student was added to the front of the queue"}

    return {"message": "No student matching provided identifier"}, 404

@blueprint.route("/end-visit", methods=["POST"])
@min_level('ta')
def end_visit():
    body = request.get_json()

    visit = body.get("id")
    reason = body.get("reason")

    if visit is None or reason is None:
        return {"message": "Malformed request"}, 400

    db.end_visit(visit, reason)

    return {"message": "Ended the visit"}



# TODO: move to end of queue (Called by TAs to add the students they just saw back to the end of the queue)


