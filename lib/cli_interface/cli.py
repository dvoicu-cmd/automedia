from .pages import CliPage
from pick import Picker
import os


class Cli:
    def __init__(self, pages: [CliPage], mapping: dict):
        """
        Rules on creating the dictionary:
        There must be a "main" key for the main menu
        Values of pages must be dicts or lists
        :param pages:
        :param mapping:
        """
        self.pages = pages
        self.mapping = mapping
        pass

    def render(self):
        main = self.mapping.get("main")
        return self.pages[main].prompt()