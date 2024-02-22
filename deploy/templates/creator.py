import os
from context import src
from context import lib
from src import *
from lib import *

manager = CreatorDirManager()
tmp = manager.create_tmp_dir()

db = DbNasConnection()

# Video editing

manager.cleanup(tmp)
