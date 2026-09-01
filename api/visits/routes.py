"""Visits Blueprint for MOH"""

from flask import Blueprint, request, g

from api.database.db import db
from api.roster.controller import min_level, get_power_level
from api.visits.controller import get_students_visit, get_tas_visit

blueprint = Blueprint("visits", __name__)


@blueprint.route("/restore-visit", methods=["GET"])
@min_level("student")
def restore_visit():
    """
    Returns a visit in the database involving the user that hasn't
    ended yet, if such a visit exists.

    i.e. if a TA refreshes the queue before ending the visit

    Returns:
        200 OK - visit found (TA)
        {
            "id": <int>,
            "username": <string>,
            "pn": <string>,
            "preferred_name: <string>,
            "visitID": <string>,
            "visit_reason": <string>
        }
        200 OK - visit found (Student)
        {
            "ta_name": <string>
        }
        404 Not Found - no such visit exists
    """
    user = g.user

    if user is None:
        return {"message": "You are not authenticated!"}, 403

    user_id = user["user_id"]

    if user["course_role"] == "student":
        visit = get_students_visit(user_id, g.course_id)
    else:
        visit = get_tas_visit(user_id, g.course_id)

    if visit is None:
        return {"message": "You do not have an in-progress visit."}, 404

    return visit


@blueprint.route("/cancel-visit", methods=["POST"])
@min_level("ta")
def cancel_visit():
    """Cancel the specified visit and return the student to the queue.

    Must be TA or higher.

    Params:
        {
            "visit_id": the id of the visit to cancel
        }

    :return: 200 with success message on success
             400 if malformed
    """
    body = request.get_json()

    visit_id = body.get("visit_id")

    if visit_id is None:
        return {"message": "Malformed request"}, 400

    db.cancel_visit(visit_id)

    return {"message": "Canceled visit"}, 200


@blueprint.route("/active-visits", methods=["GET"])
@min_level("ta")
def get_active_visits():
    """Return all incomplete visits.

    Must be TA or higher.

    :return: 200 with a list of visits formatted:
            [
                {
                    "student_id": ...,
                    "student_username": ...,
                    "student_name": ...,
                    "visitID": ...,
                    "visit_reason": ...,
                    "ta_id": ...,
                    "ta_name": ...,
                },...
            ]
    """
    in_progress = db.get_in_progress_visits(g.course_id)

    visits = []

    for visit in in_progress:
        student = db.lookup_identifier(visit["student_id"])

        if visit["ta_id"] is not None:
            ta = db.lookup_identifier(visit["ta_id"])
            ta_name = ta["preferred_name"]
        else:
            ta_name = None

        visits.append(
            {
                "student_id": visit["student_id"],
                "student_username": student["ubit"],
                "student_name": student["preferred_name"],
                "visitID": visit["visit_id"],
                "visit_reason": visit["student_visit_reason"],
                "ta_id": visit["ta_id"],
                "ta_name": ta_name,
            }
        )
    return visits


@blueprint.route("/end-visit", methods=["POST"])
@min_level("ta")
def end_visit():
    """End the specified visit.

    Must be TA or higher.

    Params:
        "id": the id of the visit
        "reason": the reason the visit ended

    :return: 200 with success message on success
             400 if malformed (visit doesn't exist, or reason is missing)
    """
    body = request.get_json()

    visit = body.get("id")
    reason = body.get("reason")

    if visit is None or reason is None:
        return {"message": "Malformed request"}, 400

    db.end_visit(visit, reason)

    return {"message": "Ended the visit"}


@blueprint.route("/visits/<user_id>", methods=["GET"])
@blueprint.route("/visits", methods=["GET"], defaults={"user_id": None})
@min_level("ta")
def get_visits(user_id):
    """
    Get a list of visits. If a user_id is specified, only include
    visits where the specified user is involved (either as the student
    or TA).

    Params:
        - user_id: <id of user involved in visit>

    Returns:
        200 on success:
            {
                "visits": [
                    {
                        "visit_id": <id of visit>,
                        "ta_id": <ta's user ID>,
                        "ta_name": <ta's first and last name>
                        "student_id": <student's user ID>,
                        "student_name": <student's first and last name>
                        "start_time": <visit start time>
                        "end_time": <visit end time>
                        "archived": <if any of the users were deleted>
                    }
                ]
            }


    :return:
    """

    user = g.user

    if (
        user["site_role"] == "admin"
        or get_power_level(user["course_role"]) > 1
        or (
            user_id is not None
            and get_power_level(user["course_role"]) > 0
            and int(user_id) == int(user["user_id"])
        )
    ):
        return {"visits": db.get_visits(g.course_id, user_id)}

    return {"message": "You are not permitted to view this resource"}, 403
