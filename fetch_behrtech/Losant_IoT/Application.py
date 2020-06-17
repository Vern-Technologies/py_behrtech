from losantrest import Client, LosantError


class Application:

    def __init__(self, app_id: str, token: str):
        self.app_id = app_id
        self.token = token

    def set_app_id(self, app_id: str):
        self.app_id = app_id

    def get_app_id(self):
        return self.app_id

    def set_token(self, token: str):
        self.token = token

    def get_token(self):
        return self.token

    @property
    def client(self) -> Client:
        return Client(auth_token=self.token)

    def test_connection(self) -> bool:
        """
        Test connection to the platform and verify provided credentials

        :return: True or False if credentials are valid
        """
        try:
            self.app_details()
            return True
        except LosantError:
            return False

    def app_details(self) -> str:
        return self.client.application.get(applicationId=self.app_id)

    def readme(self) -> str:
        return self.client.application.readme(applicationId=self.app_id)

    def app_delete(self) -> str:
        return self.client.application.delete(applicationId=self.app_id)

    def search(self, name: str) -> str:
        return self.client.application.search(applicationId=self.app_id, filter=name)


class Devices(Application):

    def device_details(self, device_id: str) -> str:
        return self.client.device.get(applicationId=self.app_id, deviceId=device_id)

    def log_entries(self, device_id: str) -> str:
        return self.client.device.get_log_entries(applicationId=self.app_id, deviceId=device_id)

    def device_update(self, device_id: str, options: dict) -> str:
        return self.client.device.patch(applicationId=self.app_id, deviceId=device_id, device=options)

    def device_delete(self, device_id: str) -> str:
        return self.client.device.delete(applicationId=self.app_id, deviceId=device_id)

    def get_recent_event(self, device_id: str) -> str:
        return self.client.device.get_state(applicationId=self.app_id, deviceId=device_id)

    def publish_event(self, device_id: str, data: list, event_id: str) -> list:
        events = [self.client.device.send_state(
            deviceId=device_id, applicationId=self.app_id, deviceState={event_id: event}) for event in data]

        return events


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
