import pdb

from .pages import CliPage
from .sigint_handling.input_cancelled import InputCancelled
from .sigint_handling.signal_handler_functions import set_watch_signal
from .sigint_handling.signal_handler_functions import reset_signal
import os
import signal
import time


class InputPage(CliPage):
    def __init__(self, title: str):
        self.title = title

    def prompt(self, default_value="", default_lock=False):
        """
        Prompts the input page
        :param default_value: sets a default value to be inputted
        :param default_lock: when set to true, bypasses the user input and sets the return value to the default_value.
        :return:
        """
        self.clear()
        i = ""  # i -> the input received

        # Attempt input
        set_watch_signal()
        try:
            # Ight gamers, check out this mental gymnastics.

            # Check if there is a lock.
            if not default_lock:  # If there is a lock, don't ask for input, skip and return the default value.

                # No default value is present, ask for an input.
                if default_value == "" or default_value is None:
                    i = input(f"{self.title}\n\n")
                # Default value present, prompt to user
                else:
                    i = input(f"{self.title}\n\nLeave blank for a default value of: \"{self.shorten_string(default_value)}\"\n\n")

            # If there is a lock, but there is no default value present, just do a regular prompt.
            elif default_value == "" or default_value is None:
                i = input(f"{self.title}\n\n")

        except InputCancelled as e:
            reset_signal()
            raise e  # Throw exception out and have who ever called it handle this exception.

        # return the default value if nothing was inputted by the user and the default values are valid.
        if i == "":
            if default_value != "" or default_value is not None:
                return default_value

        # Attempt to convert the input into an integer
        try:
            i = int(i)
        except ValueError:
            pass  # If it fails, who cares

        if isinstance(i, int):
            return int(i)  # return as an integer if it is an integer
        return i  # else return as a str

    def print_cancelled_input(self, msg='Cancelled', wait_time=0.5):
        self.clear()
        print(msg)
        time.sleep(wait_time)
        self.clear()

    @staticmethod
    def shorten_string(text, max_length=100):
        try:
            if len(text) > max_length:
                return text[:max_length - 3] + "..."
            else:
                return text
        except TypeError:  # If for some reason, text is not returned, just return the text.
            return text
