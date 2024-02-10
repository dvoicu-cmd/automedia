from abc import abstractmethod

from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

from .edit import Edit


class EndStartEdit(Edit):
    @abstractmethod
    def apply(self, composite_clip: CompositeVideoClip) -> CompositeVideoClip:
        pass

    @abstractmethod
    def duration(self) -> int:
        pass

    @abstractmethod
    def set_start_and_end(self, start_time: int, end_time: int):
        """
        Set the ending and starting times of a clip
        :param start_time:
        :param end_time:
        :return:
        """
        pass
