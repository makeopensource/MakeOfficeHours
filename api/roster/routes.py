"""Roster Blueprint for MOH"""

from flask import Blueprint, request

from api.roster.controller import min_level, add_to_roster
from api.database.db import db

blueprint = Blueprint("roster", __name__)

@min_level('instructor')
@blueprint.route("/upload-roster", methods=["POST"])
def upload_roster():
    """
        Role: instructor or admin

        Populate the database with the uploaded roster.
        Doesn't create log-ins for the users.

        Params:
            - "roster": the uploaded CSV file

        Returns:
            - 200 if successful
            - 401 if unauthorized
            - 400 if roster is missing or invalid format
    """


    if not request.files or request.files.get("roster") is None:
        return {"message": "Invalid roster upload"}, 400

    file = request.files.get("roster")
    if file.filename == '' or not file.filename.endswith(".csv"):
        return {"message": "Invalid roster upload"}, 400

    buffer = file.read()
    buffer = buffer.decode()

    lines = buffer.split("\n")
    users = []
    for line in lines:
        info = line.split(",")
        if len(info) != 4:
            return {"message": "Invalid roster upload"}, 400
        # person number needs to be numeric
        if not info[1].isnumeric():
            return {"message": "Invalid roster upload"}, 400
        pn = int(info[1])
        # role has to be valid and not above instructor's authority
        if info[3] not in {"student", "ta", "instructor"}:
            return {"message": "Invalid roster upload"}, 400

        users.append({
            "ubit": info[0],
            "pn": pn,
            "name": info[2],
            "role": info[3]
        })

    for user in users:
        add_to_roster(user["ubit"], user["pn"], user["name"], user["role"])

    return {"message": "Successfully uploaded roster"}, 200


# TODO: get roster

@min_level('instructor')
@blueprint.route("/get-roster", methods=["GET"])
def get_roster():
    """
        Role: instructor or admin

        Returns:
            401 if unauthorized
            200 if successful:
                {
                    roster: [
                        {
                            "ubit": <ubit>,
                            "pn": <person number>,
                            "name": <preferred name>,
                            "role": <user's role in course>
                    ]
                }


    """
    pass




# TODO: add to roster - to add an individual to the roster

# TODO: Remove from roster

# TODO: Whenever someone is added to the roster, check if they have an account and create one for them if not

# TODO: handle roles here (Will make it easier to move to multiple courses in the future)

