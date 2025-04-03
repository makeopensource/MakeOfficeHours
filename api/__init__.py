"""Backend api server that is used in the MOH project.

A simple flask backend that will maintaine a live queue of current students in office hours and keep
track of current student status in the within the queue
by making request updating the `vist` table within the external postgrest database.
"""

# TODO: Make the doc string sound better


import datetime
from flask import Flask, request


def create_app():
    """Create and return flask api server

    This funciton is used to setup the flask api server loading all it's depended modulars
    """
    app = Flask(__name__)

    # TODO: Basic login and signup path with session cookies

    @app.route("/health", methods=["GET"])
    def health():
        """Current health of the api server with meta data of the time and ip address"""
        # Debug only, might write a debug wrapper later
        return f"<p>Timestamp: {datetime.datetime.now().timestamp} | Server is healthy.</p>"

    @app.route("/enqueue", method=["POST"])
    def enqueue():
        """Adding students into the current live queue of the office hour

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
        """Removing the top student witin the current live queue, limited to TA only"""
        return f"{request.path} hit 😎, dequeue method is used"

    @app.route("/remove", method=["DELETE"])
    def remove():
        """Removing students from the queue base on id
        Args:
            Request.cookie: A HTTP Cookie with the name `id` for the student bring removed.
            Cookie Example -
                "id": "12344567890"

        Returns:
            A JSON of request status and possible wait time in seconds
            {
                "message": "You are enqueued",
                "wait_time": "5000"
            }
        """
        return f"{request.path} hit 😎, remove method is used."

    return app
