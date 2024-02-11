from moviepy.editor import CompositeVideoClip, ImageClip
from moviepy.video.fx.resize import resize
from src.creator.edit.end_start_edit import EndStartEdit


class AttachImage(EndStartEdit):
    def __init__(self, image_path: str, location: tuple):
        self.image = ImageClip(image_path)
        self.location = location

    def apply(self, composite_clip: CompositeVideoClip) -> CompositeVideoClip:
        output = CompositeVideoClip([composite_clip, self.image])
        return output

    def duration(self) -> int:
        return self.image.duration

    def set_start_and_end(self, start_time: int, end_time: int):
        self.image = self.image.set_start(start_time)
        self.image = self.image.set_end(end_time)

    def resize(self, height: int, width: int):
        self.image = self.image.fx(resize, height=height, width=width)
