"""Backend API server that is used in the MOH project.

A Flask API server that handles enqueuing and dequeuing students from the office hours queue.
"""

# TODO: Make the doc string sound better

import datetime
from flask import Flask, request


def create_app():
    """Create and return flask api server

    This function is used to set up the flask api server loading all it's depended on modular
    """
    app = Flask(__name__)





    @app.route("/health", methods=["GET"])
    def health():
        """Current health of the api server with metadata of the time"""
        # Debug only, might write a debug wrapper later
        return f"<p>Timestamp: {datetime.datetime.now().timestamp} | Server is healthy.</p>"

    @app.route("/enqueue", method=["POST"])
    def enqueue():
        """Add student to the current live queue for office hours

        Args:
            Request.cookie: A HTTP Cookie with the name `id` for the student bring removed.
            Cookie Example -
                "id": "12344567890" # only one field seems werid maybe more?

        Returns:
            A JSON of request status and possible wait time in seconds
            {
                "message": "You are enqueued",
                "wait_time": "5000"
            }
        """
        return f"{request.path} hit 😎, enqueue method is used"

    @app.route("/dequeue", method=["GET"])
    def dequeue():
        """Removes the top student within the current live queue, limited to TA only"""
        return f"{request.path} hit 😎, dequeue method is used"

    @app.route("/remove", method=["DELETE"])
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
