"""
Class that stores the mapping: py_file_name -> OnCalendar times
"""


import pickle
import re
import json


# TODO fix this dumb class.
# The timer is having issues with printing the map.
class TimerMap:
    def __init__(self):
        """
        Constructor method
        """
        # The data is ultimately stored as a dictionary
        self.data = {}

    def serialize(self):
        """
        Stores the contents of the mapping in a pickle file and clears them from the object
        """
        with open('timer_map.pickle', 'wb') as f:
            pickle.dump(self.data, f)
        self.data = {}

    def deserialize(self):
        """
        Loads the contents of the pickle file into the object. If no pickle file, load an empty dictionary
        """
        try:
            with open('timer_map.pickle', 'rb') as f:
                loaded_data = pickle.load(f)
                self.data = loaded_data
        except FileNotFoundError:
            # If no file, just make blank map
            self.data = {}

    def new_timer_key(self, timer_name):
        """
        Adds a new timer key to the map.

        Args:
            timer_name (str): The name of the timer to store
        """
        self.data[timer_name] = []

    def delete_timer_key(self, timer_name):
        """
        Deletes a timer key from the map.

        Args:
            timer_name (str): The name of the timer to delete.
        """
        self.__verify_key(timer_name)
        del self.data[timer_name]

    def new_exec_time_value(self, timer_name, on_calendar_values):
        """
        Append a new OnCalendar value to a timer key. Tries to ensure that there are no duplicate values to avoid conflicts

        Args:
            timer_name (str): name of the timer
            on_calendar_values (list): list of stings in the format of a calendar: DOW YYYY-MM-DD HH:MM:SS
            (see ManageService.create() for more information)
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
        """
        Gets all the execution values of a timer key

        Args:
            timer_name (str): name of the timer
        """
        self.__verify_key(timer_name)
        return self.data.get(timer_name)

    def json_return(self):
        """
        Returns the mapping in a clean json format
        """
        return json.dumps(self.data, indent=4)

    def __is_on_calendar_format(self, str_input):
        """
        A simple regex check to see if the provided string input is in general format of the systemd timers
        """
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

        Args:
            key (str): The key name
        """
        if self.data.get(key) is None:
            raise ValueError(f"{key} is not a timer/does not exists")

