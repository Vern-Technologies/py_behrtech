import requests


class ApiCall:
    """
    Is a class for connecting to and accessing messages on the gateway computers from BehrTech
    """

    def __init__(self):
        self.login_info = {}
        self.server_address = ""
        self.sensor_list = {}

    def set_login_info(self, user, password):
        """
        Sets the login credentials for the given gateway

        :param user: username credential
        :param password: password credential
        """

        self.login_info["user"] = user
        self.login_info["password"] = password

    def get_login_info(self):
        """
        Returns the login credentials for the given gateway

        :return: The login credentials for the given gatway
        """

        return self.login_info

    def set_server_address(self, server_address):
        """
        Sets the IP address for the given gateway

        :param server_address: The IP address of the given gateway
        """

        self.server_address = server_address

    def get_server_address(self):
        """
        Returns the set IP address of the gateway

        :return: The set IP address of the gateway
        """

        return self.server_address

    def set_sensor_list(self, sensor_list: dict):
        """
        Sets the sensor list of the connected sensors on the gateway. Takes in a dictionary to set multiple sensor at
        a time. Inputted dictionary should follow a given structure where each key is a sensor name and its value is the
        EUI of the sensor.

        Structure Example:  {
                                "Sensor 1": "70B3D5C1F001408D",
                                "Sensor 2": "70B3D5C1F0014054",
                                "Sensor 3": "70B3D5C1F0014056"
                            }

        :param sensor_list: Is a dictionary of the sensors connected to the gateway
        """

        for x in sensor_list:
            self.sensor_list[x] = sensor_list.get(x)

    def get_sensor_list(self):
        """
        Returns the sensor list of the given gateway

        :return: The sensor list of the given gateway
        """

        return self.sensor_list

    def fetch_jwt_token(self):
        """
        Gets the JWT token for the provided gateway that needs to be provided for getting messages from the gateway.
        The variables server_address and login_info are required to be set first before function will work.
        """

        res = requests.post(self.server_address + "/v2/login", json=self.login_info)

        if res:

            results: dict = res.json()

            return results.get("JWT")

        else:
            print("The wrong server IP address or login credentials were provided")

    def get_sensor_data(self, return_count, offset, senor_name):
        """
        Returns sensor messages from the gateway for a given sensor. The variables server_address, sensor_list,
        and jwt_token must first be set before this function will work.

        :param return_count: Is the amount of messages to be requested for the given sensor
        :param offset: Is the message count to start the message request from
        :param senor_name: Is the name of the sensor to be requested. Name should correspond to a name of a sensor in
        the set sensor_list.
        :return: the requested message from the gateway
        """

        # Retrieves the JWT Token of the gateway computer
        jwt_token = self.fetch_jwt_token()

        message = self.server_address + f"/v2/messages?returnCount={return_count}&offset={offset}&epEui=" \
                                        f"{self.sensor_list[senor_name]}"

        res = requests.get(message, headers={"Authorization": f"Bearer {jwt_token}"})

        return res
