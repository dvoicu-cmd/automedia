import os
from abc import abstractmethod
from moviepy.editor import VideoClip, AudioClip

from src.creator.edit.edit import Edit
from src.creator.canvas.canvas import CanvasInit


class VideoCompiler:

    clip: VideoClip

    def __init__(self, canvas: CanvasInit):
        """
        Inits the canvas
        :param canvas:
        """
        self.clip = canvas.init_canvas()

    def apply_edits(self, list_of_edits: [Edit]):
        """
        applies the list of edits to the clips
        :param list_of_edits:
        :return:
        """
        for edit in list_of_edits:
            self.clip = edit.apply(self.clip)

    def render(self):
        self.clip.duration = 1  # Don't remove this as it bricks the render process despite adding on edits
        self.clip.write_videofile("foo.mp4", codec='libx264', audio_codec='aac')
