"""Backend API server that is used in the MOH project.

A Flask API server that handles enqueue and dequeuing students from the office hours queue.
"""

import datetime
import io
import os
import requests
from flask import Flask, render_template, request, redirect
from flask import send_file

from api.config import config
from api.database.db import db
from api.roster.controller import min_level, get_power_level
from api.utils.debug import debug_access_only
import api.auth.routes as auth_routes
import api.queue.routes as queue_routes
import api.ratings.routes as ratings_routes
import api.roster.routes as roster_routes
import api.utils.debug_routes as debug_routes

URL_PREFIX = os.getenv("API_URL_PREFIX", "/")
THE_OG_UBIT = os.getenv("THE_OG_UBIT", None)
THE_OG_PN = os.getenv("THE_OG_PN", None)

og = db.lookup_person_number(THE_OG_PN)

def create_app():
    """Create and return Flask API server

    This function is used to set up the Flask API server, loading all its dependencies
    """

    if THE_OG_UBIT and THE_OG_PN:
        og = db.lookup_person_number(THE_OG_PN)
        if not og:
            # create the OG account
            og_id = db.create_account(THE_OG_UBIT, THE_OG_PN)
            db.add_to_roster(og_id, "admin")


    app = Flask(__name__, template_folder="../client/templates", static_folder="../client/static")

    app.config.from_object(config.Config())

    app.logger.debug(app.config)

    app.register_blueprint(auth_routes.blueprint, url_prefix=URL_PREFIX)
    app.register_blueprint(queue_routes.blueprint, url_prefix=URL_PREFIX)
    app.register_blueprint(ratings_routes.blueprint, url_prefix=URL_PREFIX)
    app.register_blueprint(roster_routes.blueprint, url_prefix=URL_PREFIX)
    app.register_blueprint(debug_routes.blueprint, url_prefix=URL_PREFIX)

    @app.route(URL_PREFIX + "/user/<user_id>", methods=["GET"])
    @min_level('ta')
    def get_user_info(user_id):
        user = db.lookup_identifier(user_id)
        return user

    @app.route(URL_PREFIX + "/me", methods=["GET"])
    def get_my_info():
        if not (auth_token := request.cookies.get("auth_token")):
            return {"message": "You are not authenticated.."}, 401

        if not (user := db.get_authenticated_user(auth_token)):
            return {"message": "You are not authenticated."}, 401

        return user

    @app.route(URL_PREFIX + "/health", methods=["GET"])
    def health():
        """Current health of the API server with metadata of the time"""
        return {"timestamp": str(datetime.datetime.now())}

    @app.route(URL_PREFIX + "/", methods=["GET"])
    def home():
        return "The API is running :)"

    return app
