import os
from context import src
from context import lib
from src import *
from lib import *

manager = PublisherDirManager()
tmp = manager.create_tmp_dir()

db = DbNasConnection()

# Scrape method of choice

# download to tmp location

# upload content

manager.cleanup(tmp)  # clean up
