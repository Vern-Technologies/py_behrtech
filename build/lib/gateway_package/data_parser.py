from datetime import datetime
import json
import os


class Parser:
    """
    Is a class for breaking the data returned from the gateway computers from BehrTech into usable components
    """

    def __init__(self):
        self.data = None

    def set_data_message(self, message):
        """
        Sets the data of the class form the message query of the gateway computer

        :param message: Is the data returned from querying the gateway computer
        """
        self.data = message

    def set_data_file(self, file_path):
        """
        Sets the data of the class loaded from a file

        :param file_path: Is the file to load data from
        """

        if os.path.exists(file_path):
            with open(file_path, "r") as file_read:
                self.data = file_read.read()

        else:
            print("Provided file path doesn't exits, pass in an absolute file path")

    def get_data(self):
        """
        Returns the data of the class

        :return: The data of the class
        """
        return self.data

    def write_data_to_file(self, file_name: str):
        """
        Outputs the data of the class to a JSON file

        :param file_name: The name of the file for the data of the class to be outputted to
        """

        text_file = open("Outputs/" + file_name + ".json", "w")
        text_file.write(self.data)

        text_file.close()

    def get_message_data(self):
        """
        Sources all the data of the class to retrieve all sensor data for each message including a time stamp and
        sensor ID

        :return: All sensor data for each message as a list
        """

        user_data = []
        count = 0
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "rxData":

                check = x.get("userDataJSON")

                if check:
                    data = json.loads(check)

                    if "message" not in data.keys():
                        user_data.append(data)
                        user_data[count]["time"] = x.get("time")
                        user_data[count]["sensorID"] = x.get("epEui")

                        count += 1

        return user_data

    def get_message_datetime_as_str(self):
        """
        Sources all the data of the class to retrieve the time stamp for each message

        :return: The time stamp of each message as a list broken into individual dicts and separated as date and time
        """

        time_info = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "rxData":

                time = x.get("time")

                if time:
                    time_split = time.strip("Z").split("T")
                    time_info.append({"date": time_split[0], "time": time_split[1]})

        return time_info

    def get_message_datetime_as_datetime(self):
        """
        Sources all the data of the class to retrieve the time stamp for each message

        :return: The time stamp of each message as a list formatted as a datetime
        """

        time_info = []
        data = json.loads(self.data)
        messages = data.get("messages")

        for x in messages:
            if x.get("command") == "rxData":

                time = x.get("time")

                if time:
                    time_split = time.strip("Z").split("T")
                    new_time = f"{time_split[0]} {time_split[1]}"
                    time_info.append(datetime.strptime(new_time, '%Y-%m-%d %H:%M:%S'))

        return time_info

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

    def get_date_ranges(self):
        """
        Sources all the data of the class to retrieve the date range of the data of the class

        :return: The date range of the data of the class as a dict
        """

        time = self.get_message_datetime_as_str()

        return {"Recent": time[0]["date"], "Oldest": time[-1]["date"]}
