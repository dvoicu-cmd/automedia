from moviepy.editor import CompositeVideoClip, CompositeAudioClip, AudioFileClip, VideoFileClip, AudioClip
from src.creator.edit.end_start_edit import EndStartEdit


class AttachVideoAudio(EndStartEdit):
    """
    Attaches the audio of a video file to the composed video.
    """
    def __init__(self, video_location: str):
        video = VideoFileClip(video_location)
        self.attach_audio = video.audio

    def apply(self, composite_clip: CompositeVideoClip) -> CompositeVideoClip:
        # Get the audio from the video file and composite clip
        existing_audio = composite_clip.audio

        if not existing_audio:  # Check if there even is audio in the current combined clip
            output = CompositeVideoClip([composite_clip.set_audio(self.attach_audio)])
            return output
        else:  # Otherwise combine the audio.
            combined_audio = CompositeAudioClip([existing_audio, self.attach_audio])
            output = CompositeVideoClip([composite_clip.set_audio(combined_audio)])
            return output

    def duration(self) -> int:
        return self.attach_audio.duration

    def set_start_and_end(self, start_time: int, end_time: int):
        self.attach_audio = self.attach_audio.set_start(start_time)
        self.attach_audio = self.attach_audio.set_end(end_time)
