from context import src
from context import lib

from src import *
from lib import *


canvas = NineBySixteen('1080x1920')
vd = VideoCompiler(canvas=canvas)


# Set up the edits
list_of_edits = []


vd.render()
