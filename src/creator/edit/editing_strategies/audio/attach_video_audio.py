from moviepy.editor import CompositeVideoClip, CompositeAudioClip, AudioFileClip, VideoFileClip, AudioClip
from src.creator.edit.edit import Edit
from .attach_audio import AttachAudio


class AttachVideoAudio(Edit):
    """
    Attaches the audio of a video file to the composed video.
    """
    def __init__(self, video_location: str):
        video = VideoFileClip(video_location)
        self.additional_audio = video.audio

    def apply(self, composite_clip: CompositeVideoClip) -> CompositeVideoClip:
        # Get the audio from the video file and composite clip
        existing_audio = composite_clip.audio

        if not existing_audio:  # Check if there even is audio in the current combined clip
            output = CompositeVideoClip([composite_clip.set_audio(self.additional_audio)])
            return output
        else:  # Otherwise combine the audio.
            combined_audio = CompositeAudioClip([existing_audio, self.additional_audio])
            output = CompositeVideoClip([composite_clip.set_audio(combined_audio)])
            return output

    def duration(self) -> int:
        return self.additional_audio.duration
