from gateway_package.Parsers.Parser import Parser
import json


class Synaptic(Parser):
    """
    Is a class for breaking the data of a Synaptic Sensor returned from a gateway computer from BehrTech into usable
    components
    """

    def __init__(self):
        Parser.__init__(self)

    def get_message_pressure(self):
        """
        Sources all the data of the class to retrieve the pressure for each message

        :return: The pressure for each message as a list
        """

        pressures = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "rxData":

                check = x.get("userDataJSON")

                if check:
                    data = json.loads(check)

                    if "message" not in data.keys():
                        pressures.append(data["Pressure"])

        return pressures

    def get_message_humidity(self):
        """
        Sources all the data of the class to retrieve the humidity for each message

        :return: The humidity for each message as a list
        """

        humidity = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "rxData":

                check = x.get("userDataJSON")

                if check:
                    data = json.loads(check)

                    if "message" not in data.keys():
                        humidity.append(data["Humidity"])

        return humidity

    def get_message_temperature(self):
        """
        Sources all the data of the class to retrieve the temperature for each message

        :return: The temperature for each message as a list
        """

        temperature = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "rxData":

                check = x.get("userDataJSON")

                if check:
                    data = json.loads(check)

                    if "message" not in data.keys():
                        temperature.append(data["Temperature"])

        return temperature

