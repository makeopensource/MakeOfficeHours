"""Queue Blueprint for MOH"""

from flask import Blueprint, request, g

from api.queue.controller import (
    remove_from_queue_without_visit,
    self_add_to_queue,
    decode_pn,
    add_to_queue_by_card_swipe,
    add_to_queue_by_ta_override,
    is_active,
)
from api.roster.controller import min_level
from api.database.db import db

blueprint = Blueprint("queue", __name__, url_prefix="/course/<course_id>")


@blueprint.route("/enqueue/swipe", methods=["POST"])
def enqueue_card_swipe():
    """
    role: hardware

    Add student to the current live queue for office hours

    Args:
        body.swipe_data: The raw data from the card swipe as a string

    Body:
        {
            "swipe_data": <string>
            "code": <string>
        }

    Returns:
        200 OK - Student was added to the queue
        400 Bad Request - Bad read
        401 Forbidden - Bad code
        404 Not Found - No student matching the card swipe was found
    """

    body = request.get_json()
    swipe_data = body["swipe_data"]
    code = body["code"]

    if code != db.get_hw_authorization():
        return {"message": "Invalid code"}, 403

    if decode_pn(swipe_data) == "":
        return {"message": "Bad read"}, 400

    if add_to_queue_by_card_swipe(swipe_data, g.course_id):
        return {"message": "Student was added to the queue"}

    return {"message": "No student matching the card swipe was found"}, 404


@blueprint.route("/enqueue/ta", methods=["POST"])
@min_level("ta")
def enqueue_ta_override():
    """
    role: TA

    Force enqueue a student.

    Resolving the id will be done in the order: UBIT -> pn -> id

    Args:
        body.identifier: A unique identifier for the student This can either be their UBIT, pn,
        or the id of their account

    Body:
        {
            "identifier": <string>
        }

    Returns:
        200 OK - Student was added to the queue
        403 Unauthorized - Requester does not have TA permissions
        404 Not Found - No student matching provided identifier
    """

    body = request.get_json()
    identifier = body["identifier"]

    if add_to_queue_by_ta_override(identifier, g.course_id):
        return {"message": "Student was added to the queue"}

    return {"message": "No student matching provided identifier"}, 404


@blueprint.route("/dequeue", methods=["POST"])
@min_level("ta")
def dequeue():
    """
    role: TA

    Remove the specified student from the queue and create a Visit in the DB. Not allowed if TA is already in a visit

    Args:
        body.id: The ID of the account to dequeue

    Body:
        "id": <string>

    Returns:
        200 OK - Student was dequeued
        {
            "id": <int>,
            "username": <string>,
            "pn": <string>,
            "preferred_name: <string>,
            "visitID": <string>,
            "visit_reason": <string>
        }

        400 Bad Request - The queue is empty or user is not in the queue
        403 Unauthorized - Requester does not have TA permissions
    """

    body = request.get_json()

    if not request.cookies.get("auth_token"):
        return {"message": "You are not logged in!"}, 403

    user = g.user
    user_id = user["user_id"]

    in_progress = db.get_in_progress_visits(g.course_id)
    in_progress = list(filter(lambda v: v["ta_id"] == user_id, in_progress))

    if len(in_progress) != 0:
        return {"message": "You have a visit in progress."}, 400

    student = db.dequeue_specified_student(body["id"], g.course_id)

    if student is None:
        return {"message": "The queue is empty"}, 400

    visit = db.create_visit(
        body["id"],
        user_id,
        student["enqueue_time"],
        student["enqueue_reason"],
        g.course_id,
    )

    return {
        "id": int(student["user_id"]),
        "username": student["ubit"],
        "pn": str(student["person_num"]),
        "preferred_name": student["preferred_name"],
        "visitID": visit,
        "visit_reason": student["enqueue_reason"],
    }


@blueprint.route("/queue", methods=["GET"])
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
        403 Forbidden - Requester does not have TA permissions
    """
    return db.get_queue(g.course_id)


@blueprint.route("/queue/size", methods=["GET"])
def get_queue_size():
    """
    Public route to get the size of queue.


    Returns:
        200 OK - {
            "size": <int>
        }
    """

    queue = db.get_queue(g.course_id)

    return {"size": len(queue)}


@blueprint.route("/queue/position", methods=["GET"])
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
            "length": <int>,
            "active": <boolean> (if the student can re-enqueue themselves)
        }
    """
    if not (auth_token := request.cookies.get("auth_token")):
        return {"message": "You are not logged in!"}, 403

    user = db.get_authenticated_user(auth_token)

    if not user:
        return {"message": "You are not logged in!"}, 403

    user_id = user["user_id"]

    queue = db.get_queue(g.course_id)

    for i, entry in enumerate(queue, 1):
        if entry["id"] == user_id:
            return {"position": i, "length": len(queue)}

    active = is_active(user_id, g.course_id)

    return {
        "message": "You are not in the queue!",
        "length": len(queue),
        "active": active,
    }, 400


@blueprint.route("/remove-self-from-queue", methods=["POST"])
def remove_self():
    """
    role: self

    Remove the requester from the queue. Creates a visit in the db to store the reason for the removal

    Args:
        Request.cookie: The auth token used to identify the requester
        body.reason: a text reason for removing the user from the queue

    Body:
        "reason": <string>


    Returns:
        200 OK - You were removed from the queue and a visit was created
        400 Bad Request - You were not in the queue
    """

    if not (auth_token := request.cookies.get("auth_token")):
        return {"message": "You are not logged in!"}, 403

    user = db.get_authenticated_user(auth_token)

    if not user:
        return {"message": "You are not logged in!"}, 403

    user_id = user["user_id"]
    body = request.get_json()

    if remove_from_queue_without_visit(
        user_id, f"[SELF-REMOVE]: {body["reason"]}", g.course_id
    ):
        return {"message": "Removed self from queue."}

    return {"message": "You are not in the queue!"}, 400


@blueprint.route("/remove-from-queue", methods=["POST"])
@min_level("ta")
def remove():
    """
    role: TA
    Removing students from the queue by id. Creates a visit in the db to store the reason for the removal

    Args:
        body.reason: a text reason for removing the user from the queue (eg. "No show")
        body.user_id: user ID of the student being removed

    Body:
        "reason": <string>,
        "user_id": <integer>

    Returns:
        200 OK - Student was removed from the queue and a visit was created
        400 Bad Request - Student with user_id was not in the queue
        403 Unauthorized - Requester does not have TA permissions
    """

    body = request.get_json()

    if body.get("user_id") is None or body.get("reason") is None:
        return {"message": "Malformed request"}, 400

    user_id = body.get("user_id")
    reason = body.get("reason")

    if remove_from_queue_without_visit(
        user_id, f"[REMOVED BY TA]: {reason}", g.course_id
    ):
        return {"message": "Removed student from queue"}
    return {"message": "Student is not in queue"}, 400


@blueprint.route("/queue", methods=["DELETE"])
@min_level("ta")
def clear_queue():
    """Removes all students from the queue
    Must be TA or higher

    :return: 200 with success message on success
    """
    db.clear_queue(g.course_id)
    return {"message": "Successfully cleared the queue."}


@blueprint.route("/enqueue/front", methods=["POST"])
@min_level("ta")
def enqueue_override_front():
    """Exact same behavior as /enqueue-ta-override, except it sends the student to the front.

    Args:
        body.identifier: A unique identifier for the student This can either be their UBIT, pn,
        or the id of their account

    Body:
        "identifier": <string>

    Returns:
        200 OK - Student was added to the queue
        403 Unauthorized - Requester does not have TA permissions
        404 Not Found - No student matching provided identifier
    """
    body = request.get_json()
    identifier = body["identifier"]

    if add_to_queue_by_ta_override(identifier, g.course_id, True):
        return {"message": "Student was added to the front of the queue"}

    return {"message": "No student matching provided identifier"}, 404


@blueprint.route("/update-reason", methods=["PATCH"])
@min_level("student")
def update_reason():
    """Update the student's reason for visiting office hours.

    Params:
        "reason": the student specified reason

    :return: 200 on success,
             401 if not authenticated,
             400 if visit is missing
    """
    body = request.get_json()

    user = g.user

    if user is None:
        return {"message": "You are not authenticated"}, 401

    reason = body.get("reason")

    if not reason:
        return {"message": "Malformed request"}, 400

    db.set_reason(user["user_id"], reason, g.course_id)

    return {"message": "Reason updated"}


@blueprint.route("/move-to-end", methods=["PATCH"])
@min_level("ta")
def move_to_end():
    """Move the specified user to the end of the queue.

    Params:
        "user_id": the id of the student to move

    :return: 200 on success,
             400 if the user doesn't exist or isn't in the queue.
    """
    body = request.get_json()

    if (user_id := body.get("user_id")) is None:
        return {"message": "Malformed request"}, 400

    if db.move_to_end(user_id, g.course_id):
        return {"message": "Moved student to end of the queue"}

    return {"message": "Specified user is not in queue"}, 400


@blueprint.route("/swipe-authorization", methods=["GET"])
@min_level("ta")
def get_swipe_auth_code():
    """Get the swipe authorization code.
    Must be TA or higher.

    :return: 200 with the authorization code as: {"code": <code>}
    """
    code = db.get_hw_authorization(g.course_id)

    if code is None:
        return {"message": "Auth code not set"}, 404

    return {"code": code}


@blueprint.route("/reset-swipe-auth", methods=["DELETE"])
@min_level("instructor")
def reset_swipe_auth_code():
    """Reset the current authorization code.

    :return: 200 with the newly generated code as: {"code": <code>}
    """
    db.reset_hw_authorization(g.course_id)

    return {"message": "Reset auth code"}


@blueprint.route("/enqueue", methods=["POST"])
@min_level("student")
def self_enqueue():
    """Attempt to self-enqueue the student who hit this endpoint.
    Fail if the student hasn't enqueued within the past two hours.

    :return: 200 on success,
             401 if the user isn't authenticated,
             403 if the user hasn't swiped within the past two hours
    """

    if not request.cookies.get("auth_token"):
        return {"message": "You are not logged in!"}, 401

    user = g.user

    if not user:
        return {"message": "You are not logged in!"}, 401

    if not self_add_to_queue(user["user_id"], g.course_id):
        return {"message": "You have not swiped in the past two hours!"}, 403

    return {"message": "Added yourself to the queue."}, 200


@blueprint.route("/queue/on-site", methods=["GET"])
@min_level("ta")
def get_on_site():
    """Return a list of students who are on-site.

    :return: 200 on success:
                [
                    {
                        "id": <int>,
                        "username": <string>,
                        "pn": <string>,
                        "preferred_name: <string>
                    },
                    ...
                ]
    """
    return db.get_on_site(g.course_id)


@blueprint.route("/deactivate", methods=["PATCH"])
@min_level("ta")
def deactivate():
    """Deactivate the specified student. Regardless of when they
    last refreshed, they should not be able to re-add themselves to
    the queue.

    Params:
        "user_id": the id of the student to deactivate.

    :return: 200 on success
    """
    body = request.get_json()
    db.reset_swipe_time(body["user_id"], g.course_id)

    return {"message": "Deactivated the student."}
