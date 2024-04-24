from moviepy.editor import CompositeVideoClip, VideoFileClip
from moviepy.video.fx.loop import loop
from moviepy.video.fx.resize import resize
from src.creator.edit.end_start_edit import EndStartEdit


class AttachLoopingVideo(EndStartEdit):
    def __init__(self, video_path: str, location: tuple):
        self.attached_video = VideoFileClip(video_path)
        self.attached_video = self.attached_video.set_audio(None)  # Mute the video. This is a must for looping vids.
        self.location = location

    def apply(self, composite_clip: CompositeVideoClip) -> CompositeVideoClip:
        self.attached_video = self.attached_video.set_position(self.location)  # apply location
        self.attached_video = self.attached_video.fx(loop)  # apply loop
        output = CompositeVideoClip([composite_clip, self.attached_video])
        return output

    def duration(self) -> int:
        return self.attached_video.duration

    def set_start_and_end(self, start_time: int, end_time: int):
        self.attached_video = self.attached_video.set_start(start_time)
        self.attached_video = self.attached_video.set_end(end_time)

    def resize(self, height: int, width: int):
        self.attached_video = self.attached_video.fx(resize, height=height, width=width)
