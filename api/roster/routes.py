"""Roster Blueprint for MOH"""

from flask import Blueprint, request, g
from api.roster.controller import min_level, add_to_roster, get_power_level
from api.database.db import db

blueprint = Blueprint("roster", __name__)

# IMPORTANT: @blueprint.route must always be outermost decorator,
# any other decorators such as, auth decorators (min_level, exact_level) must go below it


@blueprint.route("/roster", methods=["POST"])
@min_level("ta")
def upload_roster():
    """
    Role: TA or higher

    Populate the database with the uploaded roster.
    Doesn't create log-ins for the users.

    CSV formatted ubit,pn,first_name,last_name,role

    Params:
        - "roster": the uploaded CSV file

    Returns:
        - 200 if successful
        - 401 if unauthorized
        - 400 if roster is missing or invalid format
    """

    user = g.user

    if not request.files or request.files.get("roster") is None:
        return {"message": "Invalid roster upload (missing file)"}, 400

    file = request.files.get("roster")
    if file.filename == "" or not file.filename.endswith(".csv"):
        return {"message": "Invalid roster upload (invalid file)"}, 400

    buffer = file.read()
    buffer = buffer.decode()

    lines = buffer.split("\n")
    users = []
    for line in lines:
        if line == "":
            break

        info = line.strip().split(",")
        if len(info) != 5:
            return {"message": "Invalid roster upload (bad data length)"}, 400
        # person number needs to be numeric
        if not info[1].isnumeric():
            return {"message": "Invalid roster upload (non-numeric PN)"}, 400
        pn = int(info[1])
        # role has to be valid and not above user's authority
        if info[4] not in {"student", "ta", "instructor"} or get_power_level(
            info[4]
        ) >= get_power_level(user["course_role"]):
            return {"message": "Invalid roster upload (bad role)"}, 400

        users.append(
            {
                "ubit": info[0],
                "pn": pn,
                "first_name": info[2],
                "last_name": info[3],
                "role": info[4],
            }
        )

    for user in users:
        add_to_roster(
            user["ubit"],
            user["pn"],
            user["first_name"],
            user["last_name"],
            user["role"],
            g.course_id,
        )

    return {"message": "Successfully uploaded roster"}, 200


# TODO: get roster


@blueprint.route("/roster", methods=["GET"])
@min_level("ta")
def get_roster():
    """
    Role: ta, instructor, or admin

    Returns:
        401 if unauthorized
        200 if successful:
            {
                roster: [
                    {
                        "user_id": <user id>
                        "ubit": <ubit>,
                        "pn": <person number>,
                        "preferred_name": <preferred name>,
                        "last_name": <last name>
                        "role": <user's role in course>
                    }
                ]
            }


    """
    roster = db.get_roster(g.course_id)

    return {"roster": roster}


@blueprint.route("/enroll", methods=["POST"])
@min_level("ta")
def enroll_user():
    """
    Enroll a single user. Won't enroll admins. TAs can only enroll students.


    Body:
        {
            "ubit": <ubit>
            "pn": <person number>,
            "preferred_name": <preferred name>,
            "last_name": <last name>
            "role": <user's role in course>
        }

    Returns:
        200, if successful
        400, if malformed
        401, if not instructor or admin
    """
    data = request.get_json()

    user = g.user

    required_fields = ["ubit", "pn", "preferred_name", "last_name", "role"]

    legal_roles = {"student", "ta", "instructor"}

    for field in required_fields:
        if data.get(field) is None or data.get(field) == "":
            return {"message": "Malformed request"}, 400

    if data["role"] not in legal_roles:
        return {"message": "Malformed request"}, 400

    if get_power_level(data["role"]) >= get_power_level(user["course_role"]):
        return {"message": "You cannot enroll a user at this level."}, 403

    user_id = db.create_account(data["ubit"], data["pn"])
    db.add_to_roster(user_id, data["role"], g.course_id)
    db.set_initial_name(user_id, data["preferred_name"], data["last_name"])

    return {"message": "Successfully enrolled user", "id": user_id}


@blueprint.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Unenrolls the specified user.

    :return: 200 on success
             401 if removing this user isn't permitted
             404 if user doesn't exist
    """
    caller = g.user
    user = db.lookup_identifier(user_id, g.course_id)
    if get_power_level(caller["course_role"]) <= get_power_level(user["course_role"]):
        return {"message": "You cannot remove this user."}, 401

    for visit in filter(
        lambda v: int(v["student_id"]) == int(user_id)
        or int(v["ta_id"]) == int(user_id),
        db.get_in_progress_visits(g.course_id),
    ):
        db.end_visit(
            visit["visit_id"],
            "[Visit ended due to a participant's account being unenrolled.]",
        )

    db.remove_student(user_id, g.course_id)
    db.reset_swipe_time(user_id, g.course_id)

    if db.remove_from_roster(user_id, g.course_id) is None:
        return {"message": "User not found."}, 404

    return {"message": "Successfully removed user from roster"}


@blueprint.route("/user/<user_id>/role", methods=["PATCH"])
@min_level("ta")
def update_role(user_id):
    """Update the specified user's role. Can only promote people to your level.

    Body:   {
                "role": <the desired role>
            }

    :return: 200 on success
    """

    user = db.lookup_identifier(user_id, g.course_id)
    caller = g.user
    role = request.json["role"]

    if user is None:
        return {"message": "User not found."}, 401

    if role not in {"student", "ta", "instructor"}:
        return {"message": "Invalid role."}, 400

    if get_power_level(caller["course_role"]) < get_power_level(user["course_role"]):
        return {"message": "You are not permitted to change this user's role."}, 401

    if get_power_level(caller["course_role"]) < get_power_level(role):
        return {"message": "You are not permitted to set this user to this role."}, 401

    db.add_to_roster(user_id, role, g.course_id)

    return {"message": "Updated role."}


@blueprint.route("/roster", methods=["DELETE"])
@min_level("instructor")
def clear_enrollments():
    """Clear all student enrollments. This soft-deletes their accounts,
    clears the queue, etc.

    :return: 200 on success
    """
    for visit in db.get_in_progress_visits(g.course_id):
        db.end_visit(visit["visit_id"], "[Visit ended due to course reset.]")

    db.clear_queue(g.course_id)
    db.clear_on_site(g.course_id)
    db.clear_students(g.course_id)

    return {"message": "Removed all students from the course."}
