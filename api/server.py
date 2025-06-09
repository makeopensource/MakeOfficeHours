"""Backend API server that is used in the MOH project.

A Flask API server that handles enqueue and dequeuing students from the office hours queue.
"""

# TODO: Make the doc string sound better

import datetime
import io
import json
import os

import requests
from flask import Flask, request
from flask import send_file

from api.config import config
from api.utils.debug import debug_access_only
from api.database.db import create_db
import api.auth.routes as auth_routes
import api.queue.routes as queue_routes
import api.ratings.routes as ratings_routes

from api.database.db import db


def create_app():
    """Create and return Flask API server

    This function is used to set up the Flask API server, loading all its dependencies
    """
    app = Flask(__name__)

    app.config.from_object(config.Config())

    app.logger.debug(app.config)

    app.register_blueprint(auth_routes.blueprint)
    app.register_blueprint(queue_routes.blueprint)
    app.register_blueprint(ratings_routes.blueprint)

    @app.route("/", methods=["GET"])
    def home():
        mode = app.config.get("API_MODE", "Can not find API_MODE")
        return f"Welcome to the homepage, you are currently in {mode} mode"

    @app.route("/favicon.ico", methods=["GET"])
    @debug_access_only
    def favicon():
        # Timeout is in seconds
        respond = requests.get(
            "https://makeopensource.org/assets/jesse-hartloff.jpg", timeout=5
        )
        # io.BytesIO provides a byte buffer reader, very neat
        # doc: https://docs.python.org/3/library/io.html#io.BytesIO
        return send_file(io.BytesIO(respond.content), mimetype="image/jpeg")

    @app.route("/health", methods=["GET"])
    def health():
        """Current health of the API server with metadata of the time"""
        return {"timestamp": str(datetime.datetime.now())}


    return app

