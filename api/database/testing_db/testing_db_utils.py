"""Utility functions for the testing db implementation"""

import datetime

users: list[dict[str, str]] = []


def lookup_person_number(person_number) -> dict[str, str]:
    """get a user based on person number"""
    for user in users:
        if user["person_num"] == person_number:
            return user
    return {}


def lookup_identifier(identifier) -> dict[str, str]:
    """get a user based on user id, person number, or ubit"""
    for i, user in enumerate(users):
        if identifier in {user["person_num"], user["ubit"], i}:
            return user
    return {}


def timestamp():
    """generate a timestamp of the current time based on the expected format"""
    return str(datetime.datetime.now().isoformat(" ", timespec="seconds"))
