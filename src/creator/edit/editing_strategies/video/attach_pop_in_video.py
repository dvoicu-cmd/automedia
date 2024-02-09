from moviepy.editor import CompositeVideoClip, VideoFileClip
from src.creator.edit.edit import Edit


class AttachPopInVideo(Edit):
    def __init__(self, video_path: str, location: tuple):
        self.video_path = video_path
        self.location = location

    def apply(self, composite_clip: CompositeVideoClip) -> CompositeVideoClip:
        pass

    def resize_over_time(self, composite_clip: CompositeVideoClip, t):
        pass

    # https://stackoverflow.com/questions/37580910/moviepy-zooming-effects-need-tweaking
    def __resize_func(self, t, start: int, end: int):
        if t < start:
            return 1 + 0.2 * t  # zoom in
        elif end <= t <= 6:
            return 1 + 0.2 * 4  # stay
        else:
            return 1 + 0.2 * -t  # zoom out
