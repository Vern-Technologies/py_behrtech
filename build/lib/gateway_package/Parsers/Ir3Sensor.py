from gateway_package.Parsers.Parser import Parser
import json


class Ir3Sensor(Parser):
    """
    Is a class for breaking the data of a IrThermo 3 Sensor returned from a gateway computer from BehrTech into usable
    components
    """

    def __init__(self):
        Parser.__init__(self)

    def get_message_ambient_temperature(self):
        """
        Sources all the data of the class to retrieve the ambient temperature for each message

        :return: The ambient temperature for each message as a list
        """

        temperature = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "rxData":

                check = x.get("userDataJSON")

                if check:
                    data = json.loads(check)

                    if "message" not in data.keys() and "Ambient Temperature" in data.keys():
                        temperature.append(data["Ambient Temperature"])

        return temperature

    def get_message_object_temperature(self):
        """
        Sources all the data of the class to retrieve the object temperature for each message

        :return: The object temperature for each message as a list
        """

        temperature = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "rxData":

                check = x.get("userDataJSON")

                if check:
                    data = json.loads(check)

                    if "message" not in data.keys() and "Object Temperature" in data.keys():
                        temperature.append(data["Object Temperature"])

        return temperature
