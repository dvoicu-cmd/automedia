from abc import ABC, abstractmethod
from moviepy.editor import CompositeVideoClip


class Edit(ABC):
    @abstractmethod
    def apply(self, composite_clip: CompositeVideoClip) -> CompositeVideoClip:
        pass
