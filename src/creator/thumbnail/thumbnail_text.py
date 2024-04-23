import cv2
from lib.text_util.util import TextUtils


class ThumbnailText:

    text_content: str
    position: tuple  # Size 2 for x and y
    font: int
    font_scale: int
    font_color: tuple  # size 3 for RGB (except, cv2 reads as b,g,r)
    font_thickness: int
    # Background properties
    has_bg: bool  # check if a text background is enabled
    bg_padding: tuple  # (x,y) tuple determining the padding between the text and bg
    bg_color: tuple  # (r,g,b) the rgb values of the background
    bg_opacity: float  # 0 to 1 float value determining the opacity

    def __init__(self, content):
        # Default values
        self.text_content = content
        self.position = (0, 0)
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.font_scale = 6
        self.font_color = (0, 0, 0)
        self.font_thickness = self.font_scale * 2
        self.has_bg = False

    def set_background(self, padding: tuple, color: tuple, opacity: float):
        self.has_bg = True
        self.bg_padding = padding
        # For some reason cv2 reads the tuple values as (b,g,r) rather than (r,g,b). Ima just reverse the order.
        self.bg_color = tuple(reversed(color))
        self.bg_opacity = opacity

    # https://codeyarns.com/tech/2015-03-11-fonts-in-opencv.html#gsc.tab=0
    def set_font_attr(self, font: str, scale: int, thickness: int, color: tuple):
        """
        Sets the font for the thumbnail
        :param font: String with the selected font. Valid: "simplex", "plain", "duplex", "complex", "triplex", "small", "s_simplex", "s_complex"
        :param scale:
        :param thickness:
        :param color:
        :return:
        """
        valid_fonts = {
            "simplex": cv2.FONT_HERSHEY_SIMPLEX,
            "plain": cv2.FONT_HERSHEY_PLAIN,
            "duplex": cv2.FONT_HERSHEY_DUPLEX,
            "complex": cv2.FONT_HERSHEY_COMPLEX,
            "triplex": cv2.FONT_HERSHEY_TRIPLEX,
            "small": cv2.FONT_HERSHEY_COMPLEX_SMALL,
            "s_simplex": cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
            "s_complex": cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
        }
        result = valid_fonts.get(font)
        if not result:  # if there is an invalid result, use the default font.
            result = cv2.FONT_HERSHEY_PLAIN
        self.font = result
        self.font_thickness = thickness
        self.font_scale = scale
        self.font_color = tuple(reversed(color))

    def set_pos(self, x: int, y: int):
        self.position = (x, y)


    def limit_words(self, word_limit: int, new_line: int):
        """
        Limits the amount of words in a string input to make it thumbnail appropriate.
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


