from context import src
from context import lib

from src import *
from lib import *

import cv2

canvas = SixteenByNine('1920x1080')
thumb = MakeThumbnail(canvas=canvas)
thumb.place_img('/Users/dvoicu/mnt/GoofyTestFiles/minecraft parkour/Thumbnail.png', (1920, 1080), (0, 0))
thumb.place_img('/Users/dvoicu/mnt/GoofyTestFiles/minecraft parkour/gooffy ahh picture circle.png', (512, 512), (0, 0))
thumb.place_img_circle('/Users/dvoicu/mnt/GoofyTestFiles/minecraft parkour/gooffy ahh picture.jpg', 512, (0, 0))

ttxt = ThumbnailText("BF SHAT HIS PANTS AND BLAIMS ME, FOR TAKING A SHIT, WHATS GOOD MY GUYahey. yeah eh? we out here making thumbnails.")
ttxt.font = cv2.FONT_HERSHEY_PLAIN
ttxt.position = (60, 540)
ttxt.font_color = (0, 0, 0)
ttxt.font_scale = 6
ttxt.thickness = ttxt.font_scale * 2
ttxt.limit_words(16, 5)  # Each line can hold about 38 characters. average word is 4.7 characters.
thumb.place_text(ttxt)

thumb.write(2, '/Users/dvoicu/mnt/GoofyTestFiles/minecraft parkour', 'hehe')
