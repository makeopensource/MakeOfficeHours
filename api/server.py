"""Backend API server that is used in the MOH project.

A Flask API server that handles enqueue and dequeuing students from the office hours queue.
"""

import datetime

import os

from flask import Flask, request, g, abort

from api.config import config
from api.database.db import db
from api.utils import debug_routes
import api.auth.routes as auth_routes
import api.queue.routes as queue_routes
import api.roster.routes as roster_routes
import api.visits.routes as visits_routes
import api.admin.routes as admin_routes

URL_PREFIX = os.getenv("API_URL_PREFIX", "/")
THE_OG_UBIT = os.getenv("THE_OG_UBIT", None)
THE_OG_PN = os.getenv("THE_OG_PN", None)

og = db.lookup_person_number(THE_OG_PN)


def create_app():
    """Create and return Flask API server

    This function is used to set up the Flask API server, loading all its dependencies
    """

    if THE_OG_UBIT and THE_OG_PN:
        if not db.lookup_person_number(THE_OG_PN):
            # create the OG account
            og_id = db.create_account(THE_OG_UBIT, THE_OG_PN)
            db.add_to_roster(og_id, "admin")

    app = Flask(__name__)

    app.config.from_object(config.Config())

    app.logger.debug(app.config)

    app.register_blueprint(auth_routes.blueprint, url_prefix=URL_PREFIX)
    app.register_blueprint(
        queue_routes.blueprint, url_prefix=URL_PREFIX + "/course/<course_id>"
    )
    app.register_blueprint(
        roster_routes.blueprint, url_prefix=URL_PREFIX + "/course/<course_id>"
    )
    app.register_blueprint(
        debug_routes.blueprint, url_prefix=URL_PREFIX + "/course/<course_id>"
    )
    app.register_blueprint(
        visits_routes.blueprint, url_prefix=URL_PREFIX + "/course/<course_id>"
    )
    app.register_blueprint(admin_routes.blueprint, url_prefix=URL_PREFIX)

    @app.url_value_preprocessor
    def pull_info(_, values):
        """Grab the course and user info associated with this request"""
        g.course_url = values.pop("course_id", None) if values is not None else None
        g.course_context = (
            db.get_course(g.course_url) if g.course_url is not None else None
        )

        if g.course_context is not None:
            g.course_id = g.course_context["course_id"]
        else:
            g.course_id = None

        if auth_token := request.cookies.get("auth_token"):
            g.user = db.get_authenticated_user(auth_token, g.course_id)
        else:
            g.user = None

        if g.user and g.course_context:
            g.course_context["course_role"] = g.user["course_role"]

    @app.before_request
    def check_route():
        """Checks that, if this route is expecting a course, that this course exists."""
        if g.course_url is not None and not g.course_context:
            return {"message": "Course not found"}, 404
        return None

    @app.route(URL_PREFIX + "/user/<user_id>", methods=["GET"])
    def get_user_info(user_id):
        if not g.user:
            abort(403)

        user = db.lookup_identifier(user_id)

        if user is None:
            return {"message": "User not found"}, 404

        return {
            "preferred_name": user["preferred_name"],
            "last_name": user["last_name"],
            "ubit": user["ubit"],
        }

    @app.route("/course/<course_id>")
    def get_course_context():
        """Retrieve info about the specified course."""
        if g.user:
            return g.course_context
        abort(403)

    @app.route(URL_PREFIX + "/me", methods=["GET"])
    def get_my_info():
        if not request.cookies.get("auth_token"):
            return {"message": "You are not logged in."}, 401

        if not g.user:
            return {"message": "Invalid authentication."}, 401

        user = g.user | {"enrollments": db.get_enrollments(g.user["user_id"])}
        del user["course_role"]

        return user

    @app.route(URL_PREFIX + "/health", methods=["GET"])
    def health():
        """Current health of the API server with metadata of the time"""
        return {"timestamp": str(datetime.datetime.now())}

    @app.route(URL_PREFIX + "/", methods=["GET"])
    def home():
        return "The API is running :)"

    return app
