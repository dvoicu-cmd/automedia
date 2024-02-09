from context import src
from context import lib

from src import *
from lib import *


canvas = NineBySixteen('1080x1920')
vd = VideoCompiler(canvas=canvas)

# Set up the edits
edits = []

edits.append(AttachVideoAudio("/Users/dvoicu/mnt/GoofyTestFiles/Narvent, Luneex - Calm Night (4K Music Video)-uLT7DBMgD7g.mp4"))
edits.append(AttachVideoAudio("/Users/dvoicu/mnt/GoofyTestFiles/goofy ahh sounds 💀💀💀-XFirF_bFHVg.mp4"))

vd.apply_edits(edits)
vd.render()
