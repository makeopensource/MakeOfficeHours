"""Authentication controller of the

"""

from flask import Blueprint

auth = Blueprint('auth', __name__)

import api.auth.routes