import os
import sys
from abc import ABC, abstractmethod
from moviepy.editor import CompositeVideoClip, ImageClip

# Don't forget to add a context file, run this on the command line


class CanvasInit(ABC):
    @abstractmethod
    def init_canvas(self) -> ImageClip:
        pass
