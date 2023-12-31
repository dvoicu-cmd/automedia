import pickle
import re
import json


class TimerMap:
    def __init__(self):
        self.data = {}

    def serialize(self):
        with open('timer_map.pickle', 'wb') as f:
            pickle.dump(data, f)
        self.data = {}

    def deserialize(self):
        with open('timer_map.pickle', 'rb') as f:
            loaded_data = pickle.load(f)
            self.data = loaded_data

    def new_timer_key(self, timer_name):
        self.__verify_key(timer_name)
        self.data[timer_name] = []

    def delete_timer_key(self, timer_name):
        self.__verify_key(timer_name)
        del self.data[timer_name]

    def new_exec_times(self, timer_name, on_calendar_values):
        """
        Adds a new on_calendar value to a timer
        :param timer_name: name of the timer
        :param on_calendar_values: list of stings in the format: DOW YYYY-MM-DD HH:MM:SS
        """
        self.__verify_key(timer_name)

        all_values = set(self.data.values())

        for on_calendar_entry in on_calendar_values:
            # First verify format
            if self.__is_on_calendar_format(on_calendar_entry):
                # Add only if this does not conflict with any other scheduled times
                if on_calendar_entry not in all_values:
                    self.data[timer_name].append(on_calendar_entry)

    def get_exec_times(self, timer_name):
        self.__verify_key(timer_name)
        return self.data.get(timer_name)

    def json_return(self):
        return json.dumps(self.data, indent=4)

    def __is_on_calendar_format(self, str_input):
        pattern = r'^(\*|\d{1,4}|\w{3}|\d{4}-\d{2}-\d{2}|\d{2}:\d{2}:\d{2}|\~\d*|\d*\/\d+|\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})$'
        # Explanation of the pattern:
        # ^ - Start of string
        # (...)$ - Enclose the entire pattern and specify it should match the entire string

        # Use re.match to check if the string matches the pattern
        if re.match(pattern, str_input):
            return True
        else:
            return False

    def __verify_key(self, key):
        """
        Checks to see if a key input is valid. If not, raise a value error
        :param key:
        :return:
        """
        if self.data.get(key) is None:
            raise ValueError(f"{key} is not a timer/does not exists")

