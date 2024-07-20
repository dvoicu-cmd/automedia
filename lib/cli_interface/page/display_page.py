from .pages import CliPage
from .picker_pages import PickerPage


class DisplayPage(CliPage):
    """
    A type of picker page that uses the title as a descriptive note.
    """
    def __init__(self):
        pass

    def prompt(self, msg=''):
        self.clear()
        PickerPage(["continue"]).prompt(msg)  # Display

