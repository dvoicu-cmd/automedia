from abc import ABC, abstractmethod
from moviepy.editor import ImageClip


class CanvasInit(ABC):
    @abstractmethod
    def init_canvas(self) -> ImageClip:
        pass

    def canvas_path(self) -> str:
        pass
