
def add_to_queue_by_card_swipe(swipe_data):
    pass

def add_to_queue_by_ta_override(identifier):
    # identifier is resolved by checking if it's a valid UBIT, then pn, then account id
    pass


def add_to_queue(user_account):
    # called by both add_to_queue_by_card_swipe and add_to_queue_by_ta_override after user
    # has been identified and their account was pulled from the db
    pass