from .pages import CliPage
from pick import Picker


class PickerPage(CliPage):
    def __init__(self, choices: [str]):
        self.choices = choices

    def prompt(self, title='', suggested_index=-1):
        if 0 <= suggested_index < len(self.choices):  # Display suggestion
            suggested_choice = self.choices[suggested_index]
            p = Picker(self.choices, title=f"{title}  -  Suggested choice: \"{suggested_choice}\"")
            p.start()
            return p.index
        else:  # Original implementation
            p = Picker(self.choices, title=title)
            p.start()
            return p.index


