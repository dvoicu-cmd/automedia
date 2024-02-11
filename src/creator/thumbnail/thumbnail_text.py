import cv2
from lib.text_util.util import TextUtils


class ThumbnailText:

    text_content: str
    position: tuple  # Size 2 for x and y
    font: int
    font_scale: int
    font_color: tuple  # size 3 for RGB
    thickness: int

    def __init__(self, content):
        self.text_content = content
        self.position = (0, 0)
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.font_scale = 1
        self.font_color = (255, 255, 255)
        self.thickness = 2

    def limit_words(self, word_limit: int):
        self.text_content = TextUtils().split_partition_sentences(self.text_content, word_limit)[0]
        self.text_content = f"{self.text_content}..."


