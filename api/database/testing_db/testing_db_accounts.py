from api.database.idb_accounts import IAccounts


class TestingDBAccounts(IAccounts):

    def __init__(self):
        super().__init__()
        self.queue = []
        self.next_id = 0

    def create_account(self, ubit, pn):
        account_id = self.next_id
        self.next_id += 1
        return account_id
