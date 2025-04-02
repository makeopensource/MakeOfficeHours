import datetime
from flask import Flask, request

def create_app():
    app = Flask(__name__)

    @app.route("/health", methods=["GET"])
    def health():
        # Debug only, might write a debug wrapper later
        return f"<p>Timestamp: {datetime.datetime.now().timestamp} | IP: {request.remote_addr} | Server is healthy.</p>"

    return app