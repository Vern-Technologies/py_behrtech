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

    def get_all_sensor_data(self, return_count, offset):
        """
        Returns all messages from the gateway. The variable server_address must first be set before this function
        will work.

        :param return_count: Is the amount of messages to be requested
        :param offset: Is the message count to start the message request from
        :return: the requested messages from the gateway
        """

        # Retrieves the JWT Token of the gateway computer
        jwt_token = self.fetch_jwt_token()

        message = self.server_address + f"/v2/messages?returnCount={return_count}&offset={offset}"

        res = requests.get(message, headers={"Authorization": f"Bearer {jwt_token}"})

        return res

    def get_sensor_data(self, return_count, offset, senor_name):
        """
        Returns sensor messages from the gateway for a given sensor. The variable server_address must first be set
        before this function will work.

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

    def get_all_node_models(self):
        """
        Returns data on all setup node models from the gateway. The variable server_address must first be set before
        this function will work.

        :return: the requested data for all node models from the gateway
        """

        # Retrieves the JWT Token of the gateway computer
        jwt_token = self.fetch_jwt_token()

        message = self.server_address + "/v2/sensormodels"

        res = requests.get(message, headers={"Authorization": f"Bearer {jwt_token}"})

        return res

    def get_node_models(self):
        """
        Returns data on all setup node models from the gateway. The variable server_address must first be set before
        this function will work.

        :return: the requested data for all node models from the gateway
        """

        # Retrieves the JWT Token of the gateway computer
        jwt_token = self.fetch_jwt_token()

        message = self.server_address + "/v2/sensormodels"

        res = requests.get(message, headers={"Authorization": f"Bearer {jwt_token}"})

        return res

    def get_node_model(self, model_type):
        """
        Returns data on all setup node models from the gateway. The variable server_address must first be set before
        this function will work.

        :param model_type: Is the unique identifier of the node model to be requested
        :return: the requested node model data from the gateway
        """

        # Retrieves the JWT Token of the gateway computer
        jwt_token = self.fetch_jwt_token()

        message = self.server_address + f"/v2/sensormodels/{model_type}"

        res = requests.get(message, headers={"Authorization": f"Bearer {jwt_token}"})

        return res

    def get_all_nodes(self, return_count, offset):
        """
        Returns data on all connected nodes from the gateway. The variable server_address must first be set before this
        function will work.

        :param return_count: Is the amount of nodes to be requested
        :param offset: Is the node count to start the node data request from
        :return: the requested node data from the gateway
        """

        # Retrieves the JWT Token of the gateway computer
        jwt_token = self.fetch_jwt_token()

        message = self.server_address + f"/v2/nodes?returnCount={return_count}&offset={offset}"

        res = requests.get(message, headers={"Authorization": f"Bearer {jwt_token}"})

        return res

    def get_node(self, node_id):
        """
        Returns data on a requested node from the gateway. The variable server_address must first be set before this
        function will work.

        :param node_id: Is the unique identifier of the node to be requested
        :return: the requested node data from the gateway
        """

        # Retrieves the JWT Token of the gateway computer
        jwt_token = self.fetch_jwt_token()

        message = self.server_address + f"/v2/nodes/{node_id}"

        res = requests.get(message, headers={"Authorization": f"Bearer {jwt_token}"})

        return res

    def get_MQTT_mappings(self, return_count, offset):
        """
        Returns data on all setup MQTT Topics from the gateway. The variable server_address must first be set before
        this function will work.

        :param return_count: Is the amount of MQTT Topics to be requested
        :param offset: Is the MQTT Topic count to start the MQTT Topic data request from
        :return: the requested MQTT Topic data from the gateway
        """

        # Retrieves the JWT Token of the gateway computer
        jwt_token = self.fetch_jwt_token()

        message = self.server_address + f"/v2/mqttmapping?returnCount={return_count}&offset={offset}"

        res = requests.get(message, headers={"Authorization": f"Bearer {jwt_token}"})

        return res

    def get_all_MQTT_brokers(self, return_count, offset):
        """
        Returns data on all setup MQTT Brokers from the gateway. The variable server_address must first be set before
        this function will work.

        :param return_count: Is the amount of MQTT Brokers to be requested
        :param offset: Is the MQTT Broker count to start the MQTT Broker data request from
        :return: the requested MQTT Broker data from the gateway
        """

        # Retrieves the JWT Token of the gateway computer
        jwt_token = self.fetch_jwt_token()

        message = self.server_address + f"/v2/broker?returnCount={return_count}&offset={offset}"

        res = requests.get(message, headers={"Authorization": f"Bearer {jwt_token}"})

        return res

    def get_MQTT_broker(self, broker_id):
        """
        Returns data on a requested MQTT Broker from the gateway. The variable server_address must first be set before
        this function will work.

        :param broker_id: Is the unique identifier of the MQTT Broker to be requested
        :return: the requested MQTT Broker data from the gateway
        """

        # Retrieves the JWT Token of the gateway computer
        jwt_token = self.fetch_jwt_token()

        message = self.server_address + f"/v2/broker/{broker_id}"

        res = requests.get(message, headers={"Authorization": f"Bearer {jwt_token}"})

        return res

    def get_auth_ticker(self):
        """
        # TODO: Figure out what this data is used for

        :return: the requested MQTT Topic data from the gateway
        """

        # Retrieves the JWT Token of the gateway computer
        jwt_token = self.fetch_jwt_token()

        message = self.server_address + "/v2/auth/ticket"

        res = requests.get(message, headers={"Authorization": f"Bearer {jwt_token}"})

        return res

    def get_gateway_data(self):
        """
        Returns data on the gateway. The variable server_address must first be set before this function will work.

        :return: the requested gateway data
        """

        # Retrieves the JWT Token of the gateway computer
        jwt_token = self.fetch_jwt_token()

        message = self.server_address + "/v2/system"

        res = requests.get(message, headers={"Authorization": f"Bearer {jwt_token}"})

        return res

    def get_azure_mapping(self):
        """
        Returns data for setup Azure connections on the gateway. The variable server_address must first be set before
        this function will work.

        :return: the requested Azure connection data
        """

        # Retrieves the JWT Token of the gateway computer
        jwt_token = self.fetch_jwt_token()

        message = self.server_address + "/v2/azuremapping"

        res = requests.get(message, headers={"Authorization": f"Bearer {jwt_token}"})

        return res
