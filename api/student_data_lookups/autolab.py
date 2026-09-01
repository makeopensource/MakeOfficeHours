"""Functions that hit the Autolab API to retrieve user info"""

import json

import requests
from api.database.db import db
from api.auth import autolab_oauth

ROLES = {"student": "student", "course_assistant": "ta", "instructor": "ta"}


def _hit_autolab_endpoint(endpoint, access_token):
    url = f"https://autolab.cse.buffalo.edu/api/v1/{endpoint}"
    headers = {"Authorization": "Bearer " + access_token}
    try:
        response = requests.get(url, headers=headers, timeout=5.0)
    except requests.Timeout:
        return None
    return json.loads(response.content.decode())


def user_info(access_token):
    """Hits the API's user endpoint and extracts the user's information"""
    user_url = "user"
    user_data = _hit_autolab_endpoint(user_url, access_token)

    if user_data is None:
        return None

    email = user_data.get("email")
    first_name = user_data.get("first_name")
    last_name = user_data.get("last_name")
    return [email, first_name + " " + last_name]


def user_courses(user_id):
    """Hit the course endpoint and retrieve the user's course information"""
    info = db.get_autolab_info(user_id)
    if info is None:
        return []

    access_token, refresh_token = info
    courses = []

    if access_token is None:
        access_token, refresh_token, expires_in = (
            autolab_oauth.cash_in_refresh_token_for_token(refresh_token)
        )
        db.save_autolab_info(user_id, access_token, refresh_token, expires_in)

    courses_url = "courses"
    response = _hit_autolab_endpoint(courses_url, access_token)

    if response is None:
        return []

    for course in response:
        courses.append(
            {
                "course_url": course["name"],
                "course_name": course["display_name"],
                "course_sem": course["semester"],
                "course_role": ROLES.get(course["auth_level"]),
            }
        )

    return courses
