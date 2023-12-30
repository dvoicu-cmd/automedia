import pickle
import re


class TimerMap:
    def __init__(self):
        self.data = {}

    def serialize(self):
        with open('timer_map.pickle', 'wb') as f:
            pickle.dump(data, f)

    def deserialize(self):
        with open('timer_map.pickle', 'rb') as f:
            loaded_data = pickle.load(f)
            self.data = loaded_data

    def new_timer_key(self, timer_name):
        self.data[timer_name] = []

    def delete_timer_key(self, timer_name):
        self.__verify_key(timer_name)
        del self.data[timer_name]

    def new_exec_times(self, timer_name, on_calendar_values):
        self.__verify_key(timer_name)
        for on_calendar_entry in on_calendar_values:
            # First verify format
            if self.__is_on_calendar_format(on_calendar_entry):
                # Then append the value
                self.data[timer_name].append(on_calendar_entry)

    def get_exec_times(self, timer_name):
        self.__verify_key(timer_name)
        return self.data.get(timer_name)

    def __is_on_calendar_format(self, str):
        pattern = r'^(\*|\d{1,4}|\w{3}|\d{4}-\d{2}-\d{2}|\d{2}:\d{2}:\d{2}|\~\d*|\d*\/\d+|\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})$'
        # Explanation of the pattern:
        # ^ - Start of string
        # (...)$ - Enclose the entire pattern and specify it should match the entire string

        # Use re.match to check if the string matches the pattern
        if re.match(pattern, str):
            return True
        else:
            return False

    def __verify_key(self, key):
        if self.data.get(key) is None:
            raise ValueError(f"{key} is not a timer")

