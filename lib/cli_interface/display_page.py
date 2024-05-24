from .pages import CliPage
from .picker_pages import PickerPage


class DisplayPage(CliPage):
    """
    A type of picker page that uses the title as a descriptive note.
    """
    def __init__(self, page_continue: CliPage):
        """
        :param page_continue: The page to continue prompt next after the user continues.
        """
        self.contd = page_continue
        pass

    def prompt(self, msg=''):
        self.clear()
        pick_page = PickerPage(["continue"]).prompt(msg)
        self.contd.prompt()

