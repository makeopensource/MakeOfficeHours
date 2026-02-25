"""Roster Blueprint for MOH"""

from flask import Blueprint, request

from api.auth.controller import get_user
from api.roster.controller import min_level, add_to_roster
from api.database.db import db

blueprint = Blueprint("roster", __name__)

# IMPORTANT: @blueprint.route must always be outermost decorator,
# any other decorators such as, auth decorators (min_level, exact_level) must go below it

@blueprint.route("/upload-roster", methods=["POST"])
@min_level('instructor')
def upload_roster():
    """
        Role: instructor or admin

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

    print(request.files)
    if not request.files or request.files.get("roster") is None:
        return {"message": "Invalid roster upload (missing file)"}, 400

    file = request.files.get("roster")
    if file.filename == '' or not file.filename.endswith(".csv"):
        return {"message": "Invalid roster upload (invalid file)"}, 400

    buffer = file.read()
    buffer = buffer.decode()

    lines = buffer.split("\n")
    users = []
    for line in lines:
        if line == '':
            break

        info = line.strip().split(",")
        if len(info) != 5:
            return {"message": "Invalid roster upload (bad data length)"}, 400
        # person number needs to be numeric
        if not info[1].isnumeric():
            return {"message": "Invalid roster upload (non-numeric PN)"}, 400
        pn = int(info[1])
        # role has to be valid and not above instructor's authority
        if info[4] not in {"student", "ta", "instructor"}:
            return {"message": "Invalid roster upload (bad role)"}, 400

        users.append({
            "ubit": info[0],
            "pn": pn,
            "first_name": info[2],
            "last_name": info[3],
            "role": info[4]
        })

    for user in users:
        add_to_roster(user["ubit"], user["pn"], user["first_name"], user["last_name"], user["role"])

    return {"message": "Successfully uploaded roster"}, 200


# TODO: get roster

@blueprint.route("/get-roster", methods=["GET"])
@min_level('instructor')
def get_roster():
    """
        Role: instructor or admin

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
    roster = db.get_roster()

    return {"roster": roster}



@blueprint.route("/update-name", methods=["PATCH"])
@min_level('student')
def update_preferred_name():
    user = get_user(request.cookies)

    if user is None:
        return {"message": "You are not authenticated!"}, 401

    body = request.get_json()

    if (name := body.get("name")) is None:
        return {"message": "Malformed request."}, 400

    db.set_preferred_name(user["ubit"], name)

    return {"message": "Updated preferred name."}


@blueprint.route("/enroll", methods=["POST"])
@min_level('instructor')
def enroll_user():
    """
    Enroll a single user. Won't enroll admins.


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

    required_fields = ["ubit", "pn",
                       "preferred_name", "last_name",
                       "role"]

    legal_roles = {"student", "ta", "instructor"}

    for field in required_fields:
        if data.get(field) is None or data.get(field) == "":
            return {"message": "Malformed request"}, 400

    if data["role"] not in legal_roles:
        return {"message": "Malformed request"}, 400


    user_id = db.create_account(data["ubit"], data["pn"])
    db.add_to_roster(user_id, data["role"])
    db.set_name(user_id, data["preferred_name"], data["last_name"])

    return {"message": "Successfully enrolled user",
            "id": user_id}

@blueprint.route("/visits/<user_id>", methods=["GET"])
@blueprint.route("/visits", methods=["GET"], defaults={"user_id": None})
@min_level('instructor')
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
                    }
                ]
            }


    :return:
    """

    pass


# TODO: add to roster - to add an individual to the roster

# TODO: Remove from roster

# TODO: Whenever someone is added to the roster, check if they have an account and create one for them if not

# TODO: handle roles here (Will make it easier to move to multiple courses in the future)

