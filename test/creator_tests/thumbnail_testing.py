from context import src
from context import lib

from src import *
from lib import *

import cv2

canvas = SixteenByNine('1920x1080')
thumb = MakeThumbnail(canvas=canvas)
thumb.place_img('/Users/dvoicu/mnt/active/media_pools/deepfried_thumbnail_ai_img/crab_thumbnail_E5Vvv.jpg', (1920, 1080), (0, 0))

ttxt = ThumbnailText("Crab Life Secrets...")
ttxt.font = cv2.FONT_HERSHEY_TRIPLEX
ttxt.position = (60, 360)
ttxt.font_color = (128, 0, 128)
ttxt.font_scale = 4
ttxt.thickness = ttxt.font_scale * 2
ttxt.limit_words(5, 1)  # Each line can hold about 38 characters. average word is 4.7 characters.
ttxt.set_background((25,25), (255,255,0), 1)
thumb.place_text(ttxt, y_spacing=5)

thumb.write(2, '/Users/dvoicu/mnt/GoofyTestFiles', 'test_crab')
