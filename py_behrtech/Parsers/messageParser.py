
import os
import json

from requests import Response
from datetime import datetime
from .json_parsers import JSONParser
from py_behrtech.Parsers.defaults import Defaults


class MessageParser(Defaults, JSONParser):
    """
    Is the base class for breaking data returned from a gateway computer from BehrTech into usable components. Provides
    stander functions that apply to all sensor types connected to a gateway.
    """

    def __init__(self, req: Response):

        def getCount():
            count = json.loads(self.data).get('count')
            return count if count is not None else 1

        Defaults.__init__(self)
        JSONParser.__init__(self)
        self.response: Response = req
        self.data: str = req.text
        self.count = getCount()

    def get_component_data(self, component: str):
        """
        Sources all the data of the class to retrieve the data for a specified component for each message

        Example: Temperature, Pressure, etc.

        :return: The data for a specified component for each message as a list
        """

        component_data = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            check = x.get("userDataJSON")

            if check:
                data = json.loads(check)

                if "message" not in data.keys() and component in data.keys():
                    component_data.append(data[component])

        return component_data

    def get_message_data(self) -> list:
        """
        Sources all the data of the class to retrieve all sensor data for each message including a time stamp and
        sensor ID

        :return: All sensor data for each message as a list
        """

        user_data = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "ulData":

                check = x.get("userDataJSON")

                if check:
                    data = json.loads(check)

                    if "message" not in data.keys():
                        data["Time"] = x.get("time")
                        data["Command"] = x.get("command")
                        data["Type"] = x.get("type")
                        data["SensorID"] = x.get("epEui")
                        user_data.append(data)

        return user_data

    def get_all_message_types(self) -> list:
        """
        Sources all the data of the class to retrieve all messages for each message type

        :return: All messages for each message type as a list
        """

        user_data = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:

            check = x.get("userDataJSON")

            if check:
                data = json.loads(check)
                data["Time"] = x.get("time")
                data["Command"] = x.get("command")
                data["Type"] = x.get("type")
                data["SensorID"] = x.get("epEui")
                data["ID"] = x.get('_id')

            else:
                data = {"Time": x.get("time"), "Command": x.get("command"), "Type": x.get("type"),
                        "SensorID": x.get("epEui"), "ID": x.get('_id')}

            user_data.append(data)

        return user_data

    def get_message_datetime_as_str(self) -> list:
        """
        Sources all the data of the class to retrieve the time stamp for each message

        :return: The time stamp of each message as a list broken into individual dicts and separated as date and time
        """

        time_info = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            time = x.get("time")

            if time:
                time_split = time.strip("Z").split("T")
                time_info.append({"date": time_split[0], "time": time_split[1]})

        return time_info

    def get_message_datetime_as_datetime(self) -> list:
        """
        Sources all the data of the class to retrieve the time stamp for each message

        :return: The time stamp of each message as a list formatted as a datetime
        """

        time_info = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            time = x.get("time")

            if time:
                time_split = time.strip("Z").split("T")
                new_time = f"{time_split[0]} {time_split[1]}"
                time_info.append(datetime.strptime(new_time, '%Y-%m-%d %H:%M:%S'))

        return time_info

    def get_message_data_in_number_range(self, count: int, offset: int) -> list:
        """
        Sources all the data of the class to retrieve the amount of messages requested at the desired offset

        :param count: The amount of messages to be returned
        :param offset: The message position to start from
        :return: A list of the message data for the messages requested
        """

        amount = 0
        user_data = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for index, x in enumerate(messages):
            if index >= offset:
                if amount != count:
                    if x.get("command") == "ulData":

                        check = x.get("userDataJSON")

                        if check:
                            data = json.loads(check)

                            if "message" not in data.keys():
                                data["Time"] = x.get("time")
                                data["Command"] = x.get("command")
                                data["Type"] = x.get("type")
                                data["SensorID"] = x.get("epEui")
                                user_data.append(data)
                                amount += 1

                else:
                    break

        return user_data

    def get_message_data_in_date_range(self, start: datetime, end: datetime) -> list:
        """
        Sources all the data of the class to retrieve all sensor data for a message including a time stamp and
        sensor ID that is within the specified date range

        :param start: Lowest date of date range
        :param end: Highest date of date range
        :return: All sensor data for each message as a list
        """

        user_data = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "ulData":

                time = x.get("time")

                if time:
                    time_split = time.strip("Z").split("T")
                    new_time = f"{time_split[0]} {time_split[1]}"

                    message_time = datetime.strptime(new_time, '%Y-%m-%d %H:%M:%S')

                    if start <= message_time <= end:
                        check = x.get("userDataJSON")

                        if check:
                            data = json.loads(check)

                            if "message" not in data.keys():
                                data["Time"] = x.get("time")
                                data["Command"] = x.get("command")
                                data["Type"] = x.get("type")
                                data["SensorID"] = x.get("epEui")
                                user_data.append(data)

                    elif message_time < start:
                        break

        return user_data

    def get_date_ranges(self) -> dict:
        """
        Sources all the data of the class to retrieve the date range of the data of the class

        :return: The date range of the data of the class as a dict
        """

        time = self.get_message_datetime_as_str()

        return {"Recent": time[0]["date"], "Oldest": time[-1]["date"]}

    def get_message_ids(self) -> list:
        """
        Sources all the data of the class to retrieve the id for each message

        :return: The id of each message as a list
        """

        ids = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            check = x.get("_id")

            if check:
                ids.append(check)

        return ids

    def get_message_data_for_id(self, id_number) -> dict:
        """
        Sources all the data of the class to retrieve all sensor data for a message including a time stamp and
        sensor ID that matches the requested id number

        :param id_number: The id number of the message that data is being requested for
        :return: The data of the message requested for as a dictionary
        """

        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "ulData":

                check_id = x.get("_id")

                if check_id:
                    if check_id == id_number:

                        check_data = x.get("userDataJSON")

                        if check_data:
                            data = json.loads(check_data)

                            if "message" not in data.keys():
                                data["Time"] = x.get("time")
                                data["Command"] = x.get("command")
                                data["Type"] = x.get("type")
                                data["SensorID"] = x.get("epEui")
                                return data

    def get_message_position_for_id(self, id_number) -> int:
        """
        Sources all the data of the class to retrieve the position of the message that matches the requested id number

        :param id_number: The id number of the message that data is being requested for
        :return: The position of the messages that matches the requested id number
        """

        data = json.loads(self.data)
        messages = data.get("messages")

        for index, x in enumerate(messages):

            check_id = x.get("_id")

            if check_id:
                if check_id == id_number:
                    return index + 1

    def get_message_epEui(self) -> list:
        """
        Sources all the data of the class to retrieve the epEui for each message

        :return: The epEui of each message as a list
        """

        ids = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "ulData":

                check = x.get("epEui")

                if check:
                    ids.append(check)

        return ids

    def get_message_data_for_epEui(self, eui_number) -> list:
        """
        Sources all the data of the class to retrieve all sensor data for a message including a time stamp and
        sensor ID that matches the requested epEui number

        :param eui_number: The epEui number of the message that data is being requested for
        :return: The data of the message requested for as a dictionary
        """

        user_data = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "ulData":

                check_eui = x.get("epEui")

                if check_eui:
                    if check_eui == eui_number:

                        check_data = x.get("userDataJSON")

                        if check_data:
                            data = json.loads(check_data)

                            if "message" not in data.keys():
                                data["Time"] = x.get("time")
                                data["Command"] = x.get("command")
                                data["Type"] = x.get("type")
                                data["SensorID"] = x.get("epEui")
                                user_data.append(data)

        return user_data

    def get_message_position_for_epEui(self, eui_number) -> int:
        """
        Sources all the data of the class to retrieve the position of the message that matches the requested epEui
        number

        :param eui_number: The epEui number of the message that data is being requested for
        :return: The position of the messages that matches the requested epEui number
        """

        data = json.loads(self.data)
        messages = data.get("messages")

        for index, x in enumerate(messages):

            check_eui = x.get("epEui")

            if check_eui:
                if check_eui == eui_number:
                    return index + 1
