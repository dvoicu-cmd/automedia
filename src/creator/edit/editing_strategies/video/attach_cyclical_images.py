from moviepy.editor import CompositeVideoClip, VideoFileClip, ImageSequenceClip
from moviepy.video.fx.loop import loop
from moviepy.video.fx.resize import resize
from src.creator.edit.end_start_edit import EndStartEdit
from lib.manage_directory_structure.dir_manager import DirManager


class AttachCyclicalImages(EndStartEdit):

    def __init__(self, images: list, duration_between_img: int, location: tuple):
        # Then populate a list containing the duration between each img in sec.
        duration_between = []
        for i in range(len(images)):
            duration_between.append(duration_between_img)

        self.image_seq = ImageSequenceClip(images, durations=duration_between)
        self.location = location

    def set_location(self, location: tuple):
        self.location = location

    def apply(self, composite_clip: CompositeVideoClip) -> CompositeVideoClip:
        self.image_seq = self.image_seq.set_position(self.location)  # apply location
        self.image_seq = self.image_seq.fx(loop)  # apply loop effect
        output = CompositeVideoClip([composite_clip, self.image_seq])
        return output

    def duration(self) -> int:
        return self.image_seq.duration

    def set_start_and_end(self, start_time: int, end_time: int):
        self.image_seq = self.image_seq.set_start(start_time)
        self.image_seq = self.image_seq.set_end(end_time)
