from moviepy.editor import CompositeVideoClip, CompositeAudioClip, AudioFileClip
from src.creator.edit.edit import Edit


class AttachAudio(Edit):
    """
    Attaches audio to the composed video from an audio file.
    """
    def __init__(self, audio_location: str):
        self.attach_audio = AudioFileClip(audio_location)

    def apply(self, composite_clip: CompositeVideoClip) -> CompositeVideoClip:
        existing_audio = composite_clip.audio
        if not existing_audio:  # Check if there even is audio in the current combined clip
            output = CompositeVideoClip([composite_clip.set_audio(self.attach_audio)])
            return output
        else:  # Otherwise combine the audio
            composite_audio = CompositeAudioClip([composite_clip.audio, self.attach_audio])
            output = CompositeVideoClip([composite_clip.set_audio(composite_audio)])
            return output

    def duration(self) -> int:
        return self.attach_audio.duration
