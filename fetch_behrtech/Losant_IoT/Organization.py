
from losantrest import Client


class Organization:

    def __init__(self, org_id: str, token: str):
        self.org_id = org_id
        self.token = token

    def set_org_id(self, org_id: str):
        self.org_id = org_id

    def get_org_id(self):
        return self.org_id

    def set_token(self, token: str):
        self.token = token

    def get_token(self):
        return self.token

    @property
    def client(self):
        return Client(auth_token=self.token)

    def org_details(self):
        return self.client.org.get(orgId=self.org_id)
