from .pages import CliPage
from .picker_pages import PickerPage
import textwrap
import os
from lib.text_util.util import TextUtils


class DisplayPage(CliPage):
    """
    A type of picker page that uses the title as a descriptive note.
    """
    def __init__(self):
        pass

    @staticmethod
    def get_lines(title):
        terminal_width = os.get_terminal_size().columns
        wrapped_title = textwrap.fill(title, terminal_width)
        return wrapped_title

    def prompt(self, msg=''):
        self.clear()
        input(f"{msg}\n\n Press Enter to continue.")



