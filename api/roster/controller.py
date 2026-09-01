"""Roster related functions and permission-checking decorators for the API"""

from functools import wraps
from flask import request, current_app, g

from api.database.db import db


def get_power_level(role):
    """Returns the numerical power level of each role"""
    match role:
        case "student":
            return 0
        case "ta":
            return 1
        case "instructor":
            return 5
        case "admin":
            return 10
    return -1


def exact_level(role):
    """Ensures that only the role specified has access to a feature. It is very important that these
    decorators are below @blueprint.route, as they are otherwise ignored."""

    def decorator(f):
        @wraps(f)
        def check_permission(*args, **kwargs):
            if current_app.config.get("API_MODE", "") == "testing":
                return f(*args, **kwargs)

            if g.user and g.user["site_role"] == "admin":
                return f(*args, **kwargs)

            if not (auth_token := request.cookies.get("auth_token")):
                return {"message": "You are not authenticated"}, 403

            user = db.get_authenticated_user(auth_token, g.course_id)

            if not user:
                return {"message": "You are not authenticated"}, 403

            if role == user["course_role"]:
                return f(*args, **kwargs)

            return {
                "message": "You do not have permission to access this resource"
            }, 403

        return check_permission

    return decorator


def min_level(min_role):
    """Allows for specified level and above to access features. It is very important that these decorators are
    below @blueprint.route, as they are otherwise ignored."""

    def decorator(f):
        @wraps(f)
        def check_permission(*args, **kwargs):
            if current_app.config.get("API_MODE", "") == "testing":
                return f(*args, **kwargs)

            if not request.cookies.get("auth_token"):
                return {"message": "You are not authenticated"}, 403

            required_level = get_power_level(min_role)

            user = g.user

            if not user:
                return {"message": "You are not authenticated"}, 403

            if user["site_role"] == "admin":
                return f(*args, **kwargs)

            power_level = get_power_level(user["course_role"])

            if power_level >= required_level:
                return f(*args, **kwargs)

            return {
                "message": "You do not have permission to access this resource"
            }, 403

        return check_permission

    return decorator


def authenticated():
    """Require some authentication to access this route."""

    def decorator(f):
        @wraps(authenticated)
        def check_auth(*args, **kwargs):
            if g.user:
                return f(*args, **kwargs)
            return {"message": "You are not authenticated."}, 401

        return check_auth

    return decorator


def site_admin_only(f):
    """Require site-wide admin to access this route"""

    @wraps(f)
    def check_auth(*args, **kwargs):
        if g.user and g.user["site_role"] == "admin":
            return f(*args, **kwargs)
        return {"message": "You are not permitted to access this resource."}, 403

    return check_auth


def add_to_roster(ubit, pn, first_name, last_name, role, course):
    """Adds a student to the roster with the following information: UBIT,
    person number, first name, last name, role"""
    user_id = db.create_account(ubit, pn)
    db.add_to_roster(user_id, role, course)
    db.set_initial_name(user_id, first_name, last_name)
