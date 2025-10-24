"""Authentication Blueprint for MOH"""

from flask import Blueprint

blueprint = Blueprint("auth", __name__)


@blueprint.route("/login", methods=["POST"])
def login():
    """Checks if the current user has the right credentials to log in
    Args:
        email: forum data field of email
        password: forum data field of password

    Returns:
        The status of the login attempt
    """
    return "Login arrived"


@blueprint.route("/signup", methods=["POST"])
def signup():
    """Creates an account using the given credentials,
    fails if email already registered for an account
    Args:
        email: forum data field of email
        password: forum data field of password

    Returns:
        The status of the sign-up attempt
    """
    return "Signup arrived"

# TODO: update preferred name

# TODO: accounts has UBIT (For AL lookups) and pn (For card swipes)
