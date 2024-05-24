from abc import ABC, abstractmethod
import os


class CliPage(ABC):
    @abstractmethod
    def prompt(self):
        pass

    @staticmethod
    def clear():
        size = os.get_terminal_size()
        num_lines = size[1]
        while num_lines >= 0:
            print("\n")
            num_lines -= 1
