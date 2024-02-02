from .pages import CliPage
from pick import Picker


class PickerPage(CliPage):
    def __init__(self, choices: [str]):
        self.choices = choices

    def prompt(self):
        p = Picker(self.choices)
        p.start()
        return p.index


