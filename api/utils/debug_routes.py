from api.database.db import db
from flask import request, Blueprint
from api.auth.controller import create_account
from api.utils.debug import debug_access_only

blueprint = Blueprint("debug", __name__)

@blueprint.route("/force-enroll", methods=["POST"])
@debug_access_only
def force_enroll():
    body = request.form
    ubit = body.get("ubit")
    pn = body.get("pn")
    role = body.get("role")

    if role not in {"student", "ta", "instructor", "admin"}:
        return {"message": "Invalid role"}, 400

    print(role)
    user_id = create_account(ubit, pn, role)

    return {"message": "Successfully enrolled", "id": user_id}