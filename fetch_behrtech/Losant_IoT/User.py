
from losantrest import Client


class User:

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def set_email(self, email: str):
        self.email = email

    def get_email(self):
        return self.email

    def set_password(self, password: str):
        self.password = password

    def get_password(self):
        return self.password

    @property
    def client(self) -> Client:
        client = Client()
        response = client.auth.authenticate_user(credentials={'email': self.email, 'password': self.password})
        client.auth_token = response['token']
        return client

    def create_application(self, name: str, description: str) -> str:
        return self.client.applications.post(application={"name": name, "description": description})

    def get_applications(self) -> str:
        return self.client.applications.get()
