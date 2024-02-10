from context import src
from context import lib

from src import *
from lib import *


canvas = NineBySixteen('1080x1920')
vds1 = VideoSection(canvas=canvas)

# Set up the edits
edits = []

e1 = AttachVideo("/Users/dvoicu/mnt/GoofyTestFiles/Narvent, Luneex - Calm Night (4K Music Video)-uLT7DBMgD7g.mp4", ('center',0))
e1.set_start_and_end(2, e1.duration())
edits.append(e1)
e2 = AttachVideo("/Users/dvoicu/mnt/GoofyTestFiles/Edging my Brain AAUUGHeurysm-MnX2XOjdcWg.mp4", ('center','center'))
edits.append(e2)

vds1.apply_edits(edits, e2)

vds2 = VideoSection(canvas=canvas)
edits = []
e2.set_start_and_end(0,2)
edits.append(e2)
e1.set_start_and_end(2,100)
edits.append(e1)

vds2.apply_edits(edits, e1)


vds1.concat(vds2)
vds1.render()
