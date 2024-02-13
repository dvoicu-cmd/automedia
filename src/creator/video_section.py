# MoviePy
from moviepy.editor import VideoClip, concatenate_videoclips, concatenate_audioclips

# Custom
from src.creator.edit.edit import Edit
from src.creator.edit.end_start_edit import EndStartEdit
from src.creator.canvas.canvas import CanvasInit


class VideoSection:

    clip: VideoClip

    def __init__(self, canvas: CanvasInit):
        """
        Initialize the clip section with a set canvas size.
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
        self.clip = self.clip.subclip(0, duration_edit.duration())

    def concat(self, other: 'VideoSection'):
        """
        Concatenates another video section to the end of this section's video section.
        :param other:
        :return:
        """
        other_clip = other.clip
        this_clip = self.clip

        # handle video
        concatenated_video = concatenate_videoclips([this_clip, other_clip])

        # handle audio
        if this_clip.audio is not None and other_clip.audio is not None:  # In case of mute sections to prevent err.
            concatenated_audio = concatenate_audioclips([this_clip.audio, other_clip.audio])
            concatenated_video = concatenated_video.set_audio(concatenated_audio)

        # Set pointer
        self.clip = concatenated_video


    def render(self, output_path):
        """
        Renders the video clip
        :param output_path: The absolute path for the output video.
        :return:
        """
        self.clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
