from . import auth


@auth.route("/login", methods=["POST"])
def login():
    """Checks if the current user has the right credentials to log in
    Args:
        email: forum data field of email
        password: forum data field of password

    Returns:
        The status of the login attempt
    """
    return "Login arrived"


@auth.route("/signup", method=["POST"])
def signup():
    """Creates an account using the given credentials,
    fails if email already registered for an account
    Args:
        email: forum data field of email
        password: forum data field of password

    Returns:
        The status of the signup attempt
    """
    return "Signup arrived"
