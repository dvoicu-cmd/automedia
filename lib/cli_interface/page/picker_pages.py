from .pages import CliPage
from pick import Picker


class PickerPage(CliPage):
    def __init__(self, choices: [str]):
        self.choices = choices

    def prompt(self, title=''):
        p = Picker(self.choices, title=title)
        p.start()
        return p.index


