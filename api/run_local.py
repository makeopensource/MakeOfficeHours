"""Runs the app locally without Gunicorn. To be used for dev and testing"""

from dotenv import load_dotenv  # pylint: disable=wrong-import-position

load_dotenv()

from api.server import create_app  # pylint: disable=wrong-import-position

app = create_app()
app.debug = True
app.run(port=5050)
