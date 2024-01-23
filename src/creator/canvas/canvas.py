import os
import sys
from abc import ABC, abstractmethod
from moviepy.editor import CompositeVideoClip, ImageClip

from src.creator.video_compiler import VideoCompiler  # Don't forget to add a context file, run this on the command line


class CanvasInit(ABC):
    @abstractmethod
    def init_canvas(self) -> ImageClip:
        pass
