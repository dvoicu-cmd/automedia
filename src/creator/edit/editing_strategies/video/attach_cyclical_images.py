from moviepy.editor import CompositeVideoClip, VideoFileClip, ImageSequenceClip
from moviepy.video.fx.loop import loop
from moviepy.video.fx.resize import resize
from src.creator.edit.end_start_edit import EndStartEdit
from lib.manage_directory_structure.dir_manager import DirManager


class AttachCyclicalImages(EndStartEdit):

    def __init__(self, images: list, duration_between_img: int, location: tuple):
        # Then populate a list containing the duration between each img in sec.
        duration_between = []
        duration_total = 0
        for i in range(len(images)):
            duration_between.append(duration_between_img)
            duration_total = duration_total + duration_between_img

        self.image_seq = ImageSequenceClip(images, durations=duration_between)
        self.image_seq = self.image_seq.set_duration(duration_total)
        self.location = location

    def set_location(self, location: tuple):
        self.location = location

    def apply(self, composite_clip: CompositeVideoClip) -> CompositeVideoClip:
        self.image_seq = self.image_seq.set_position(self.location)  # apply location
        # Applying the loop effect sets the duration to None.
        # If you what to re-use the object, store the duration before applying.
        tmp_duration = self.duration()
        self.image_seq = self.image_seq.fx(loop)
        output = CompositeVideoClip([composite_clip, self.image_seq])
        # Before giving the output clip, set the duration back to its original value.
        self.image_seq = self.image_seq.set_duration(tmp_duration)
        return output

    def duration(self) -> int:
        return self.image_seq.duration

    def set_start_and_end(self, start_time: int, end_time: int):
        self.image_seq = self.image_seq.set_start(start_time)
        self.image_seq = self.image_seq.set_end(end_time)
