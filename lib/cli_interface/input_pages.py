from .pages import CliPage
import os


class InputPage(CliPage):
    def __init__(self, title: str):
        self.title = title

    def prompt(self):
        self.__clear()
        i = input(f"{self.title}\n\n")
        return i

    def __clear(self):
        size = os.get_terminal_size()
        num_lines = size[1]
        while num_lines >= 0:
            print("\n")
            num_lines -= 1
