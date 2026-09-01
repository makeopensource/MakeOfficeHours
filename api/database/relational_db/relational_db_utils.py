"""Utilities for the database implementation"""

import datetime


def to_str_timestamp(offset=0):
    """generate a timestamp of the current time based on the expected format"""
    time = datetime.datetime.now() + datetime.timedelta(seconds=offset)
    return str(time.isoformat(" ", timespec="seconds"))
