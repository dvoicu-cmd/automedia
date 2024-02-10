from moviepy.editor import VideoClip, concatenate_videoclips

from src.creator.edit.edit import Edit
from src.creator.edit.end_start_edit import EndStartEdit
from src.creator.canvas.canvas import CanvasInit


class VideoSection:

    clip: VideoClip

    def __init__(self, canvas: CanvasInit):
        """
        Inits the canvas
        :param canvas:
        """
        self.clip = canvas.init_canvas()

    def clip(self):
        return self.clip

    def apply_edits(self, list_of_edits: [Edit], duration_edit: EndStartEdit):
        """
        applies the list of edits to the clips
        :param list_of_edits:
        :param duration_edit: The edit that determines the entire duration of the combined clip
        :return:
        """
        for edit in list_of_edits:
            self.clip = edit.apply(self.clip)

        # Now subclip and cut the duration
        # The five is for test purposes, replace.
        self.clip = self.clip.subclip(0, 5)  # duration_edit.duration()

    def concat(self, other: 'VideoSection'):
        """
        Concatenates another video section to the end of this section's video section.
        :param other:
        :return:
        """
        other_clip = other.clip
        self.clip = concatenate_videoclips([self.clip, other_clip])

    def render(self):
        self.clip.write_videofile("foo.mp4", codec='libx264', audio_codec='aac')
