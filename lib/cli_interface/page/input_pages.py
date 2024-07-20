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

    def prompt(self):
        self.clear()
        i = ""

        # Attempt input
        set_watch_signal()
        try:
            i = input(f"{self.title}\n\n")
        except InputCancelled as e:
            reset_signal()
            raise e  # Throw exception out and have who ever called it handle this exception.

        # Attempt to convert the input into an integer
        try:
            i = int(i)
        except ValueError:
            pass  # If it fails, who cares

        if isinstance(i, int):
            return int(i)  # return as an integer if it is an integer
        return i  # else return as a str

    def print_cancelled_input(self):
        self.clear()
        print("Cancelled")
        time.sleep(0.5)
        self.clear()
