"""Routes for use by administrator page"""

from flask import Blueprint, request, g

from api.roster.controller import site_admin_only
from api.database.db import db

blueprint = Blueprint("admin", __name__)


@blueprint.route("/course", methods=["POST"])
@site_admin_only
def create_course():
    """Admin only route to create a new course.

    Params:
        - name
        - semester
        - url
    """

    json = request.get_json()

    try:
        json["url"].encode("ascii")
    except UnicodeEncodeError:
        return {"message": "Invalid course URL."}, 400

    course = db.create_course(json["name"], json["semester"], json["url"])

    if course == -1:
        return {"message": "Failed to create course, uniqueness failed"}, 400

    return db.get_course(course)


@blueprint.route("/courses", methods=["GET"])
@site_admin_only
def get_courses():
    """Retrieves all courses"""
    return {"courses": db.get_courses()}


@blueprint.route("/user", methods=["POST"])
@site_admin_only
def create_user():
    """Creates a normal user.

    Params:
        "ubit": <ubitname>
        "pn": <person number>
        "first_name": <preferred name>
        "last_name": <surname>
    """
    json = request.get_json()

    if not all(key in json for key in ["ubit", "pn", "first_name", "last_name"]):
        return {"message": "Malformed request"}, 400

    user = db.create_account(json["ubit"], json["pn"])
    db.set_initial_name(user, json["first_name"], json["last_name"])

    return {"user": user}


@blueprint.route("/course/<course_id>/appoint", methods=["POST"])
@site_admin_only
def create_instructor():
    """Appoints a user to be the instructor of a course.
    This user must already exist.

    Params:
        course_id: ID of the course
        ubit: UBIT of the instructor to promote
    :return:
    """
    json = request.get_json()

    user = db.lookup_identifier(json["ubit"])

    if not user:
        return {"message": "User not found"}, 404

    db.add_to_roster(user["user_id"], "instructor", g.course_id)
    return {"message": "Enrolled user as an instructor."}
