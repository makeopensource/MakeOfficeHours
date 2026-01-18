from api.database.db import db
from functools import wraps
from flask import request, current_app

def get_power_level(role):
    match role:
        case "student":
            return 0
        case "ta":
            return 1
        case "instructor":
            return  5
        case "admin":
            return 10
    return -1

def exact_level(role):
    def decorator(f):
        @wraps(f)
        def check_permission(*args, **kwargs):
            if current_app.config.get("API_MODE", "") == "testing":
                return f(*args, **kwargs)

            if not (auth_token := request.cookies.get("auth_token")):
                return {"message": "You are not authenticated"}, 403

            user = db.get_authenticated_user(auth_token)

            if not user:
                return {"message": "You are not authenticated"}, 403

            if role == user["role"]:
                return f(*args, **kwargs)

            return {
                "message": "You do not have permission to access this resource"
            }, 403

        return check_permission

    return decorator


def min_level(min_role):
    def decorator(f):
        @wraps(f)
        def check_permission(*args, **kwargs):
            if current_app.config.get("API_MODE", "") == "testing":
                return f(*args, **kwargs)

            if not (auth_token := request.cookies.get("auth_token")):
                return {"message": "You are not authenticated"}, 403

            required_level = get_power_level(min_role)

            user = db.get_authenticated_user(auth_token)

            if not user:
                return {"message": "You are not authenticated"}, 403

            power_level = get_power_level(user["course_role"])

            if power_level >= required_level:
                return f(*args, **kwargs)

            return {
                "message": "You do not have permission to access this resource"
            }, 403

        return check_permission

    return decorator

def add_to_roster(ubit, pn, first_name, last_name, role):
    user_id = db.create_account(ubit, pn)
    db.add_to_roster(user_id, role)
    db.set_name(user_id, first_name, last_name)