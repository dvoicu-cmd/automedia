from abc import ABC, abstractmethod
from moviepy.editor import CompositeVideoClip


class Edit(ABC):
    @abstractmethod
    def apply(self, composite_clip: CompositeVideoClip) -> CompositeVideoClip:
        """
        The application of the edit to the composite clip
        :param composite_clip:
        :return: Composite video clip with the edit attached.
        """
        pass

    @abstractmethod
    def duration(self) -> int:
        """
        Returns the duration of a specific edit
        :return: integer value of the duration
        """
        pass
