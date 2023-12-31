import pickle
import re
import json


class TimerMap:
    def __init__(self):
        self.data = {}

    def serialize(self):
        with open('timer_map.pickle', 'wb') as f:
            pickle.dump(self.data, f)
        self.data = {}

    def deserialize(self):
        try:
            with open('timer_map.pickle', 'rb') as f:
                loaded_data = pickle.load(f)
                self.data = loaded_data
        except FileNotFoundError:
            # If no file, just make blank map
            self.data = {}

    def new_timer_key(self, timer_name):
        self.data[timer_name] = []

    def delete_timer_key(self, timer_name):
        self.__verify_key(timer_name)
        del self.data[timer_name]

    def new_exec_time_value(self, timer_name, on_calendar_values):
        """
        Adds a new on_calendar value to a timer
        :param timer_name: name of the timer
        :param on_calendar_values: list of stings in the format: DOW YYYY-MM-DD HH:MM:SS
        """
        self.__verify_key(timer_name)

        all_values = list(self.data.values())

        for on_calendar_entry in on_calendar_values:
            # First verify format
            if self.__is_on_calendar_format(on_calendar_entry):
                # Add only if this does not conflict with any other scheduled times
                for this_key_list in all_values:  # All values is a list of lists for each key
                    if on_calendar_entry in this_key_list:
                        break
                    else:
                        self.data[timer_name].append(on_calendar_entry)

    def get_exec_times(self, timer_name):
        self.__verify_key(timer_name)
        return self.data.get(timer_name)

    def json_return(self):
        return json.dumps(self.data, indent=4)

    def __is_on_calendar_format(self, str_input):
        # Checks for the pattern YYYY-MM-DD HH:MM:SS
        pattern1 = r'[0-9*\/\.]+-[0-9*\/\.]+-[0-9*\/\.]+ [0-9*\/\.]+:[0-9*\/\.]+:[0-9*\/\.]+'
        # Check for the pattern DOW HH:MM:SS
        pattern2 = r'[A-Z][a-z][a-z] [0-9*\/\.]+:[0-9*\/\.]+:[0-9*\/\.]+'

        # Use re.match to check if the string matches the pattern
        if re.match(pattern1, str_input) or re.match(pattern2, str_input):
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

