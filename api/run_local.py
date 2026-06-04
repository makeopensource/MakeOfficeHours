"""Runs the app locally without Gunicorn. To be used for dev and testing"""

from dotenv import load_dotenv

from api.server import create_app

load_dotenv()


app = create_app()
app.debug = True
app.run(port=5050)
