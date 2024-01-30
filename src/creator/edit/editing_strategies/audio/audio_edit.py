from moviepy.editor import CompositeVideoClip, AudioClip

from src.creator.edit.edit import Edit


class AppendAudio(Edit):

    def __init__(self, audio_location: str):
        self.audio_location = audio_location

    def apply(self, composite_clip: CompositeVideoClip) -> CompositeVideoClip:
        audio = AudioClip(self.audio_location)
        output = CompositeVideoClip([composite_clip.set_audio(audio)])
        return output
