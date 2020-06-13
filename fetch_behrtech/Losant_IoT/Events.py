from losantrest import Client


class Events:

    def __init__(self, device_id: str, key: str, secret: str):
        self.device_id = device_id
        self.key = key
        self.secret = secret

    def set_device_id(self, device_id: str):
        self.device_id = device_id

    def get_device_id(self):
        return self.device_id

    def set_key(self, key: str):
        self.key = key

    def get_key(self):
        return self.key

    def set_secret(self, secret: str):
        self.secret = secret

    def get_secret(self):
        return self.secret

    def publish_event(self, data: list, event_id: str):
        """
        Publishes device data to the Losant IoT Platform

        :param data: List of Device json data messages
        :param event_id: Event topic to publish at
        """

        client = Client()
        response = client.auth.authenticate_device(
            credentials={'deviceId': self.device_id, 'key': self.key, 'secret': self.secret})

        client.auth_token = response['token']
        app_id = response['applicationId']

        if app_id is not None:

            events = [client.device.send_state(
                deviceId=self.device_id, applicationId=app_id, deviceState={event_id: event}) for event in data]

            return events
