"""Util functions that will be used for debugging only within flask debug mode"""

from functools import wraps
from flask import current_app, abort


# Referenced: https://stackoverflow.com/a/55729767
def debug_access_only(func):
    """Limit route access to debug mode only, return 404 if access outside of debug mode.
    Must cognizant of the order decorators are declared. Decorators that limit route
    access must be declared after @blueprint.route.
    """

    @wraps(func)
    def wrapped(**kwargs):
        if current_app.debug:
            return func(**kwargs)
        return abort(404)

    return wrapped
