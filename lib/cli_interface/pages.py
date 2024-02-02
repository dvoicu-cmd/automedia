from abc import ABC, abstractmethod


class CliPage(ABC):
    @abstractmethod
    def prompt(self):
        pass
