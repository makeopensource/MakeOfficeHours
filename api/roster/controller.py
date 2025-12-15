from api.database.db import db
from functools import wraps
from flask import request, current_app


def permission_required(min_role):
    def decorator(f):
        @wraps(f)
        def check_permission(*args, **kwargs):
            if current_app.config.get("API_MODE", "") == "testing":
                return f(*args, **kwargs)

            if not (auth_token := request.cookies.get("auth_token")):
                return {"message": "You are not authenticated"}, 403

            required_level = 0
            match min_role:
                case "ta":
                    required_level = 1
                case "instructor":
                    required_level = 5
                case "admin":
                    required_level = 10

            user = db.get_authenticated_user(auth_token)

            if not user:
                return {"message": "You are not authenticated"}, 403

            power_level = 0
            match user["course_role"]:
                case "ta":
                    power_level = 1
                case "instructor":
                    power_level = 5
                case "admin":
                    power_level = 10

            if power_level >= required_level:
                return f(*args, **kwargs)

            return {
                "message": "You do not have permission to access this resource"
            }, 403

        return check_permission

    return decorator
