"""Backend API server that is used in the MOH project.

A Flask API server that handles enqueue and dequeuing students from the office hours queue.
"""

# TODO: Make the doc string sound better

import datetime
import io
import json

import requests
from flask import Flask, request
from flask import send_file

from api.config import config
from api.utils.debug import debug_access_only


def create_app():
    """Create and return Flask API server

    This function is used to set up the Flask API server, loading all its dependencies
    """
    app = Flask(__name__)

    app.config.from_object(config.Config())

    app.logger.debug(app.config)

    @app.route("/", methods=["GET"])
    def home():
        return f"Welcome to the homepage, you are currently in \
{app.config.get("API_MODE", "Can not find API_MODE")}"

    @app.route("/favicon.ico", methods=["GET"])
    @debug_access_only
    def favicon():
        # Timeout is in seconds
        respond = requests.get(
            "https://makeopensource.org/assets/jesse-hartloff.jpg", timeout=5
        )
        # io.BytesIO provides a byte buffer reader, very neat
        # doc: https://docs.python.org/3/library/io.html#io.BytesIO
        return send_file(io.BytesIO(respond.content), mimetype="image")

    @app.route("/health", methods=["GET"])
    def health():
        """Current health of the API server with metadata of the time"""
        # Debug only, might write a debug wrapper later
        app.logger.debug(datetime.datetime.now().timestamp())
        return {"timestamp": str(datetime.datetime.now())}

    @app.route("/enqueue", methods=["POST"])
    def enqueue():
        """Add student to the current live queue for office hours

        Args:
            Request.cookie: A HTTP Cookie with the name `id` for the student bring removed.
            Cookie Example -
                "id": "12344567890" # only one field seems weird maybe more?

        Returns:
            A JSON of request status and possible wait time in seconds
            {
                "message": "You are enqueued",
                "wait_time": "5000"
            }
        """
        return f"{request.path} hit 😎, enqueue method is used"

    @app.route("/dequeue", methods=["DELETE"])
    def dequeue():
        """Removes the top student within the current live queue, limited to TA only"""
        return f"{request.path} hit 😎, dequeue method is used"

    @app.route("/remove", methods=["DELETE"])
    def remove():
        """Removing students from the queue based on id
        Args:
            Request.cookie: A HTTP Cookie with the name `id` for the student bring removed.
            Cookie Example -
                "id": "12344567890"

        Returns:
            A JSON of request status
            {
                "message": "You are removed from the queue"
            }
        """
        return f"{request.path} hit 😎, remove method is used."

    return app
