
from losantrest import Client, LosantError


class Application:
    """
    Application specific actions on the Losant IoT Platform
    """

    def __init__(self, app_id: str, token: str):
        self.app_id = app_id
        self.token = token

    def set_app_id(self, app_id: str):
        """
        Set the app_id of the class

        :param app_id:  Application ID from the Losant IoT Platform
        """
        self.app_id = app_id

    def get_app_id(self):
        """
        Gets the app_id of the class

        :return: The value of the app_id of the class
        """
        return self.app_id

    def set_token(self, token: str):
        """
        Set the token of the class

        :param token: Token key from the Losant IoT Platform
        """
        self.token = token

    def get_token(self):
        """
        Gets the token of the class

        :return: The value of the token of the class
        """
        return self.token

    @property
    def client(self) -> Client:
        """
        Sets up a Client connection to the Losant IoT Platform

        :return: A Client object
        """
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
        """
        Provides details for the connected Application from the Losant IoT Platform

        :return: JSON string of application details
        """
        return self.client.application.get(applicationId=self.app_id)

    def readme(self) -> str:
        """
        Gets the README of the connected Application from the Losant IoT Platform

        :return: String of the README file of the connected Application
        """
        return self.client.application.readme(applicationId=self.app_id)

    def app_delete(self) -> str:
        """
        Deletes the connected Application from the Losant IoT Platform

        :return: String of deletion status
        """
        return self.client.application.delete(applicationId=self.app_id)

    def search(self, name: str) -> str:
        """
        Gets details on a resource on the Losant IoT Platform

        :param name: Name of resource requesting details for
        :return: String of details for the requested resource
        """
        return self.client.application.search(applicationId=self.app_id, filter=name)


class Devices(Application):
    """
    Device specific actions of the Losant IoT Platform
    """

    def device_details(self, device_id: str) -> str:
        """
        Gets details on a specified device

        :param device_id: ID of the device requesting for
        :return: String of details for the requested device
        """
        return self.client.device.get(applicationId=self.app_id, deviceId=device_id)

    def log_entries(self, device_id: str, limit: int = 1) -> str:
        """
        Gets the most recent log entries for the requested device

        :param device_id: ID of the device requesting for
        :param limit: The amount of log entries to request for
        :return: String of the requested log entries
        """
        return self.client.device.get_log_entries(applicationId=self.app_id, deviceId=device_id, limit=limit)

    def device_update(self, device_id: str, options: dict) -> str:
        """
        Updates information about a device

        :param device_id: ID of the device to update for
        :param options: Dictionary of new properties for the device
        :return: String of update status
        """
        return self.client.device.patch(applicationId=self.app_id, deviceId=device_id, device=options)

    def device_delete(self, device_id: str) -> str:
        """
        Deletes a device

        :param device_id: ID of the device to be deleted
        :return: String of deletion status
        """
        return self.client.device.delete(applicationId=self.app_id, deviceId=device_id)

    def get_recent_event(self, device_id: str, limit: int = 1) -> str:
        """
        Gets the last know states of the device

        :param device_id: ID of the device to get states for
        :param limit: The amount of states to request for
        :return: String of states request status
        """
        return self.client.device.get_state(applicationId=self.app_id, deviceId=device_id, limit=limit)

    def publish_event(self, device_id: str, data: list) -> list:
        """
        Publishes device data to the Losant IoT Platform

        Example of data format:
            With time: [{'time': '2020-06-15T18:48:52Z', 'data': {etc. sensor attributes}}]
            Without time: [{'data': {etc. sensor attributes}}]

        :param device_id: ID of device to push data to
        :param data: List of Device json data messages
        :return:
        """

        events = []

        for event in data:
            if 'time' in event.keys():
                events.append(self.client.device.send_state(deviceId=device_id, applicationId=self.app_id, deviceState={
                        'time': event['time'], 'data': event['data']}))
            else:
                events.append(self.client.device.send_state(deviceId=device_id, applicationId=self.app_id, deviceState={
                    'data': event['data']}))

        return events
