from moviepy.editor import CompositeVideoClip, ImageClip
from src.creator.edit.edit import Edit


class AttachImage(Edit):
    def __init__(self, image_path: str, location: tuple):
        self.image_path = image_path
        self.location = location

    def apply(self, composite_clip: CompositeVideoClip) -> CompositeVideoClip:
        img = ImageClip(self.image_path)
        output = CompositeVideoClip([composite_clip, img])
        return output

    def duration(self) -> int:
        pass
