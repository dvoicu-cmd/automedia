from context import src
from context import lib

from src import *
from lib import *

txt = ThumbnailText("HELLO SHIT ASS")
txt.position = (100, 100)


thumb = MakeThumbnail(SixteenByNine('1920x1080'))
thumb.place_img('/Users/dvoicu/mnt/GoofyTestFiles/Lyra IV.png', (512, 512), (100, 100))
thumb.place_text(txt)

thumb.write(5, '/Users/dvoicu/mnt/GoofyTestFiles', 'Thumb')



