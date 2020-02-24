import uuid
import yaml
import os
import wiotp.sdk.application as ibm_app
import wiotp.sdk.exceptions as ibm_exceptions


class Devices:
    """
    Is a class that interfaces with IBM's Python package to manage devices and device types
    """

    def __init__(self, key: str, token: str):
        self.key = key
        self.token = token

    def set_key(self, key: str):
        """
        Sets the key of the class

        :param key: ID for a API Key on IBM Watson IoT Platform
        """

        self.key = key

    def get_key(self):
        """
        Gets the key of the class

        :return: ID for a API Key on IBM Watson's IoT Platform
        """

        return self.key

    def set_token(self, token: str):
        """
        Sets the token of the class

        :param token: ID for a API token on IBM Watson IoT Platform
        """

        self.token = token

    def get_token(self):
        """
       Gets the token of the class

       :return: ID for a API token on IBM Watson's IoT Platform
       """

        return self.token

    @property
    def doc(self):
        """
        Connections document for connecting to a API on IBM Watson's IoT Platform
        """

        doc = dict(
            identity=dict(
                appId=str(uuid.uuid4())
            ),
            auth=dict(
                key=self.key,
                token=self.token
            ),
            options=dict(
                domain='internetofthings.ibmcloud.com',
                logLevel='debug',
                http=dict(
                    verify=True
                ),
                mqtt=dict(
                    port=8883,
                    transport='tcp',
                    cleanStart=True,
                    keepAlive=60
                )
            )
        )

        return doc

    def test_connection(self):
        """
        Checks for a connection to the IBM Watson IoT Platform

        :return:
        """

        # Creates a yaml file on system at package root to pass to ibm application parse configuration
        with open('app.yaml', 'w') as outfile:
            yaml.dump(self.doc, outfile, default_flow_style=False)

        options = ibm_app.parseConfigFile("app.yaml")
        client = ibm_app.ApplicationClient(config=options, logHandlers=None)

        client.connect()

        # Remove generated app configuration file
        os.remove('app.yaml')

        return client.isConnected()

    def verify_device_type(self, type_id: str):
        """
        Verifies that a device type exist on IBM Watson's IoT Platform

        :param type_id: The ID of the device type to verify for
        :return: Boolean value if device type exist or not
        """

        # Creates a yaml file on system at package root to pass to ibm application parse configuration
        with open('app.yaml', 'w') as outfile:
            yaml.dump(self.doc, outfile, default_flow_style=False)

        options = ibm_app.parseConfigFile("app.yaml")
        client = ibm_app.ApplicationClient(config=options, logHandlers=None)

        # Remove generated app configuration file
        os.remove('app.yaml')

        try:
            if client.registry.devicetypes[type_id]:
                return True

        except KeyError:
            print(f"Device type {type_id} does not exist")
            return False

    def get_all_device_types(self):
        """
        Builds a list of all device types on IBM Watson's IoT Platform

        :return: A list of all device types on IBM Watson's IoT Platform
        """

        # Creates a yaml file on system at package root to pass to ibm application parse configuration
        with open('app.yaml', 'w') as outfile:
            yaml.dump(self.doc, outfile, default_flow_style=False)

        options = ibm_app.parseConfigFile("app.yaml")
        client = ibm_app.ApplicationClient(config=options, logHandlers=None)

        # Remove generated app configuration file
        os.remove('app.yaml')

        device_list = [device_type for device_type in client.registry.devicetypes]

        if device_list is not None:
            return device_list

        else:
            print("No device types exist")
            return None

    def delete_device_type(self, type_id: str):
        """
        Deletes a device type from IBM Watson's IoT Platform

        :param type_id: The ID of the device type to delete for
        :return: Boolean value if device type was deleted or not
        """

        # Creates a yaml file on system at package root to pass to ibm application parse configuration
        with open('app.yaml', 'w') as outfile:
            yaml.dump(self.doc, outfile, default_flow_style=False)

        options = ibm_app.parseConfigFile("app.yaml")
        client = ibm_app.ApplicationClient(config=options, logHandlers=None)

        # Remove generated app configuration file
        os.remove('app.yaml')

        if self.verify_device_type(type_id=type_id):

            try:
                client.registry.devicetypes.delete(typeId=type_id)

                print(f"Device type deleted for {type_id}")
                return True

            except ibm_exceptions.ApiException:
                print(f"Device type for {type_id} can not be deleted")
                return False

        else:
            return False

    def create_device_type(self, type_id: str, description: str = ""):
        """
        Creates a device type on IBM Watson's IoT Platform

        :param type_id: The ID for the device type to be create
        :param description: A description of the device to be created
        :return: Boolean value if device type was created or not
        """

        # Creates a yaml file on system at package root to pass to ibm application parse configuration
        with open('app.yaml', 'w') as outfile:
            yaml.dump(self.doc, outfile, default_flow_style=False)

        options = ibm_app.parseConfigFile("app.yaml")
        client = ibm_app.ApplicationClient(config=options, logHandlers=None)

        # Remove generated app configuration file
        os.remove('app.yaml')

        if not self.verify_device_type(type_id=type_id):

            client.registry.devicetypes.create({"id": type_id, "description": description})
            print(f"Device type created for {type_id}")
            return True

        else:
            print(f"Device type {type_id} already exists")
            return False

    def verify_device(self, device_id: str):
        """
        Verifies if a device exist or not on IBM Watson's IoT Platform

        :param device_id: The ID of the device to verify for
        :return: Boolean if device exist or not
        """

        # Creates a yaml file on system at package root to pass to ibm application parse configuration
        with open('app.yaml', 'w') as outfile:
            yaml.dump(self.doc, outfile, default_flow_style=False)

        options = ibm_app.parseConfigFile("app.yaml")
        client = ibm_app.ApplicationClient(config=options, logHandlers=None)

        # Remove generated app configuration file
        os.remove('app.yaml')

        for device in client.registry.devices:
            if device['deviceId'] == device_id:
                return device

        print(f"Device {device_id} does not exist")
        return False

    def create_device(self, type_id: str, device_id: str):
        """
        Creates a device on IBM Watson's IoT Platform

        :param type_id: The ID of the device type for the device to be created
        :param device_id: The ID of the device to be created
        :return: The results for creating a new device
        """

        # Creates a yaml file on system at package root to pass to ibm application parse configuration
        with open('app.yaml', 'w') as outfile:
            yaml.dump(self.doc, outfile, default_flow_style=False)

        options = ibm_app.parseConfigFile("app.yaml")
        client = ibm_app.ApplicationClient(config=options, logHandlers=None)

        # Remove generated app configuration file
        os.remove('app.yaml')

        if self.verify_device_type(type_id=type_id):

            if not self.verify_device(device_id=device_id):

                result = client.registry.devices.create({"typeId": type_id, "deviceId": device_id})

                if result.success:
                    return result

                else:
                    print(f"Device unable to be created for TypeId {type_id} and DeviceId {device_id}")
                    return None

            else:

                print(f"Device {device_id} already exist")
                return None

        else:
            print(f"Provided device type {type_id} does not exist")
            return None

    def delete_device(self, device_id: str):
        """
        Deletes a device from IBM Watson's IoT Platform

        :param device_id: The ID of the device to be deleted
        :return: Boolean value if device was deleted or not
        """

        # Creates a yaml file on system at package root to pass to ibm application parse configuration
        with open('app.yaml', 'w') as outfile:
            yaml.dump(self.doc, outfile, default_flow_style=False)

        options = ibm_app.parseConfigFile("app.yaml")
        client = ibm_app.ApplicationClient(config=options, logHandlers=None)

        # Remove generated app configuration file
        os.remove('app.yaml')

        for device in client.registry.devices:
            if device['deviceId'] == device_id:

                return client.registry.devices.delete({"deviceId": device_id})

        print(f"Device {device_id} does not exist")
        return False

    def get_all_devices(self):
        """
        Builds a list of all devices on IBM Watson's IoT Platform

        :return: A list of all devices on IBM Watson's IoT Platform
        """

        # Creates a yaml file on system at package root to pass to ibm application parse configuration
        with open('app.yaml', 'w') as outfile:
            yaml.dump(self.doc, outfile, default_flow_style=False)

        options = ibm_app.parseConfigFile("app.yaml")
        client = ibm_app.ApplicationClient(config=options, logHandlers=None)

        # Remove generated app configuration file
        os.remove('app.yaml')

        device_list = [device for device in client.registry.devices]

        if device_list is not None:
            return device_list

        else:
            print("No devices exist")
            return None
