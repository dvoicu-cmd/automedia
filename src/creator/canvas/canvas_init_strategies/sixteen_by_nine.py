import os
from moviepy.editor import ImageClip
from src.creator.canvas.canvas import CanvasInit


class SixteenByNine(CanvasInit):
    def __init__(self, resolution: str):
        package_directory = os.path.dirname(__file__)
        self.image_path = os.path.join(package_directory, 'aspect_ratios', '16:9', f'{resolution}.png')
        if not os.path.exists(self.image_path):
            raise ValueError(f"Invalid resolution:{resolution}")

    def init_canvas(self) -> ImageClip:
        clip = ImageClip(img=self.image_path)
        clip.fps = 60
        return clip

    def canvas_path(self) -> str:
        return self.image_path
