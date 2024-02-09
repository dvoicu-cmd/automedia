from moviepy.editor import CompositeVideoClip
import cv2

from src.creator.edit.edit import Edit


class AttachBlur(Edit):
    def __init__(self):
        pass

    def apply(self, composite_clip: CompositeVideoClip) -> CompositeVideoClip:
        output = composite_clip.fl_image(self.__blur)
        return output

    @staticmethod
    def __blur(image):
        """ Returns a blurred (radius=2 pixels) version of the image """
        return cv2.GaussianBlur(image, (5, 5), 0)

