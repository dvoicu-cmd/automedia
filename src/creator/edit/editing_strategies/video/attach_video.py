from moviepy.editor import CompositeVideoClip
from src.creator.edit.edit import Edit


class AttachVideo(Edit):
    def __init__(self, video_path: str, location: tuple):
        self.video_path = video_path
        self.location = location


    def apply(self, composite_clip: CompositeVideoClip) -> CompositeVideoClip:
        pass

