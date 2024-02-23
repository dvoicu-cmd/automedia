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

    def limit_words(self, word_limit: int, new_line: int):
        """

        :param word_limit: The number of words limited
        :param new_line: After x many words, add in a new line
        :return:
        """
        # Chop off words
        words = TextUtils().split_single_words(self.text_content)
        words = words[:word_limit]

        # Reconstruct and format the string
        txt = ''
        i = 0
        for word in words:
            if i == new_line:
                txt = f"{txt} {word}\n"
                i = 0
            else:
                txt = f"{txt} {word}"
                i += 1
        # End with ellipsis
        txt = txt + '...'
        self.text_content = txt


