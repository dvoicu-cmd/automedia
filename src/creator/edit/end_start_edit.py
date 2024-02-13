from abc import abstractmethod

from .edit import Edit


class EndStartEdit(Edit):
    @abstractmethod
    def set_start_and_end(self, start_time: int, end_time: int):
        """
        Set the ending and starting times of a clip
        :param start_time:
        :param end_time:
        :return:
        """
        pass
