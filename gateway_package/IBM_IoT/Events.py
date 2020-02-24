import os
import yaml
import wiotp.sdk.device as ibm_device


class Events:
    """
    Is a class that interfaces with IBM's Python package to publish and subscribe to events on their IoT Platform
    """

    def __init__(self, org_id: str, type_id: str, device_id: str, token: str):
        self.org_id = org_id
        self.type_id = type_id
        self.device_id = device_id
        self.token = token

    def set_org_id(self, org_id: str):
        """
        Sets the org_id of the class

        :param org_id: ID for IBM Watson IoT Platform organization
        """

        self.org_id = org_id

    def get_org_id(self):
        """
        Gets the org_id of the class

        :return: ID for IBM Watson IoT Platform organization
        """

        return self.org_id

    def set_type_id(self, type_id: str):
        """
        Sets the type_id of the class

        :param type_id: The ID of a device type on IBM Watson's IoT Platform
        """

        self.type_id = type_id

    def get_type_id(self):
        """
        Gets the type_id of the class

        :return: ID for a device type on IBM Watson's IoT Platform
        """

        return self.type_id

    def set_device_id(self, device_id: str):
        """
        Sets the device_id of the class

        :param device_id: The ID of a device on IBM Watson's IoT Platform
        """

        self.device_id = device_id

    def get_device_id(self):
        """
        Gets the device_id of the class

        :return: ID for a device on IBM Watson's IoT Platform
        """

        return self.device_id

    def set_token(self, token: str):
        """
        Sets the token of the class

        :param token: The token ID of a device on IBM Watson's IoT Platform
        """

        self.token = token

    def get_token(self):
        """
        Gets the token of the class

        :return: ID token for a device on IBM Watson's IoT Platform
        """

        return self.token

    @property
    def doc(self):
        """
        Connections document for connecting to a device on IBM Watson's IoT Platform
        """

        doc = dict(
            identity=dict(
                orgId=self.org_id,
                typeId=self.type_id,
                deviceId=self.device_id
            ),
            auth=dict(
                token=self.token
            ),
            options=dict(
                domain='internetofthings.ibmcloud.com',
                logLevel='debug',
                mqtt=dict(
                    port=8883,
                    transport='tcp',
                    cleanStart=True,
                    keepAlive=60
                )
            )
        )

        return doc

    def publish_event(self, data: list, event_id: str) -> list:
        """
        Publishes device data to the IBM Watson IoT Platform

        :param data: List of Device json data messages
        :param event_id: Event topic to publish at
        """

        # Creates a yaml file on system at package root to pass to ibm device parse configuration
        with open('device.yaml', 'w') as outfile:
            yaml.dump(self.doc, outfile, default_flow_style=False)

        options = ibm_device.parseConfigFile('device.yaml')
        client = ibm_device.DeviceClient(config=options, logHandlers=None)

        client.connect()

        if client.isConnected():

            events = [client.publishEvent(eventId=event_id, msgFormat="json", data=event, qos=0, onPublish=None)
                      for event in data]

            os.remove('device.yaml')

            return events

