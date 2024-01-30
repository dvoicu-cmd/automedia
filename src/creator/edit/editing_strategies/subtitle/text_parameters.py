class TextParam:
    def __init__(self):
        self._font = 'times'
        self._size = 24
        self._color = 'white'
        self._bg_color = 'transparent'
        self._outline_color = 'black'
        self._outline_width = 12

    @property
    def font(self):
        return self._font

    @property
    def size(self):
        return self._size

    @property
    def color(self):
        return self._color

    @property
    def bg_color(self):
        return self._bg_color

    @property
    def outline_color(self):
        return self._outline_color

    @property
    def outline_width(self):
        return self._outline_width

    def set_font(self, font_name, size):
        self._font = font_name
        self._size = size

    def set_font_color(self, color, bg_color):
        self._color = color
        self._bg_color = bg_color

    def set_font_outline(self, color, size):
        self._outline_color = color
        self._outline_width = size
