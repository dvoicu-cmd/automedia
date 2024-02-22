import os
from context import src
from context import lib
from src import *
from lib import *

manager = ScraperDirManager()
tmp = manager.create_tmp_dir()

db = DbNasConnection()

scrapes = None  # Scrape method of choice

manager.dl_text("sample", "sample", tmp)  # download to tmp location

files = manager.select_dir(tmp)  # gather files

for file in files:  # upload them
    db.create_media_file(file, "sample", "sample", "sample", "sample")

manager.cleanup(tmp) # clean up
