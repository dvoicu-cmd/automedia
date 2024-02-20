from .pages import CliPage
import os


class InputPage(CliPage):
    def __init__(self, title: str):
        self.title = title

    def prompt(self):
        self.clear()
        i = input(f"{self.title}\n\n")
        return i
