from context import src
from context import lib

from src import *
from lib import *


canvas = NineBySixteen('1080x1920')
vdsBase = VideoSection(canvas=canvas)

# Set up the edits
edits = []

e1 = AttachAudio('/Users/dvoicu/mnt/GoofyTestFiles/AUUGHHH Tik Tok Sound Effect.mp3')
e1.set_start_and_end(0, e1.duration())

e2 = AttachImage('/Users/dvoicu/mnt/GoofyTestFiles/Lyra IV.png', ('center','center'))
e2.set_start_and_end(3, 6)

edits.append(e1)
edits.append(e2)


vdsBase.apply_edits(edits, e1)

vds1 = VideoSection(canvas=canvas)

edits = []

e1 = AttachMuteVideo('/Users/dvoicu/mnt/GoofyTestFiles/Edging my Brain AAUUGHeurysm-MnX2XOjdcWg.mp4', ('center','top'))
e1.set_start_and_end(0, e1.duration())

e2 = AttachLoopingVideo('/Users/dvoicu/mnt/GoofyTestFiles/Funniest 5 Second Video Ever!-YKsQJVzr3a8.mp4', ('center','bottom'))
e2.set_start_and_end(0, e1.duration())

e3 = AttachVideoAudio('/Users/dvoicu/mnt/GoofyTestFiles/Narvent, Luneex - Calm Night (4K Music Video)-uLT7DBMgD7g.mp4')
e3.set_start_and_end(0, e3.duration())

edits.append(e1)
edits.append(e2)
edits.append(e3)

vds1.apply_edits(edits, e1)

vdsBase.concat(vds1)

vdsBase.render()





