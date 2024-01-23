from moviepy.editor import VideoFileClip
import cv2


class Blur:
    def __init__(self):
        pass

    def apply(self, clip_location):
        clip = VideoFileClip(clip_location)
        clip = clip.fl_image(self.__blur)
        return clip

    @staticmethod
    def __blur(image):
        """ Returns a blurred (radius=2 pixels) version of the image """
        return cv2.GaussianBlur(image, (5, 5), 0)

