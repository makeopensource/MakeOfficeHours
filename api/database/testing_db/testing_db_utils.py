users: list[dict[str, str]] = []


def lookup_person_number(person_number) -> dict[str, str]:
    for user in users:
        if user["person_num"] == person_number:
            return user
    return {}


def lookup_identifier(identifier) -> dict[str, str]:
    for i, user in enumerate(users):
        if identifier in {user["person_num"], user["ubit"], i}:
            return user
    return {}