from moviepy.editor import CompositeVideoClip, CompositeAudioClip, AudioFileClip
from src.creator.edit.edit import Edit


class AttachAudio(Edit):
    """
    Attaches audio to the composed video from an audio file.
    """
    def __init__(self, audio_location: str):
        self.audio_location = audio_location

    def apply(self, composite_clip: CompositeVideoClip) -> CompositeVideoClip:
        attach_audio = AudioFileClip(self.audio_location)
        composite_audio = CompositeAudioClip([composite_clip.audio, attach_audio])
        output = CompositeVideoClip([composite_clip.set_audio(composite_audio)])
        return output
