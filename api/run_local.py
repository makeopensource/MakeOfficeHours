# Runs the app locally without Gunicorn. To be used for dev and testing

from dotenv import load_dotenv

load_dotenv()

from api.server import create_app

app = create_app()
app.run()
