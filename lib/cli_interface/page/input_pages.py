from .pages import CliPage
import os


class InputPage(CliPage):
    def __init__(self, title: str):
        self.title = title

    def prompt(self):
        self.clear()
        i = input(f"{self.title}\n\n")

        try:
            i = int(i)
        except ValueError:
            pass

        if isinstance(i, int):
            return int(i)  # return as an integer if it is an integer
        return i  # else return as a str
