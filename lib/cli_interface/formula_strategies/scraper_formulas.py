import os
import sys

from lib.manage_formula.manage_formula import ManageFormula
from lib.cli_interface.input_pages import InputPage
from lib.cli_interface.picker_pages import PickerPage


class ScraperFormulas:
    def __init__(self):
        pass

    @staticmethod
    def reddit_scrape():
        f = ManageFormula()

        name = InputPage("Input the name of the service").prompt()
        desc = InputPage("Input the description for the scrapes").prompt()
        subreddit = InputPage("Input the subreddit name").prompt()
        media_pool = InputPage("Input the corresponding media_pool").prompt()

        f.ap(f"""
        
manager = ScraperDirManager()
tmp = manager.create_tmp_dir()

db = DbNasConnection()

scrapes = RedditScrape().scrape("{subreddit}", "hot", "text", 1, 5)
        
        """)

        # This is stupid, but it works.
        s = f'manager.dl_list_of_text(scrapes, f"{subreddit}_'
        s = s + '{manager.get_rand_id()}", tmp)'
        f.ap(s)

        f.ap(f"""
        
files = manager.select_dir(tmp)

for file in files:
    db.create_media_file(file, "text", os.path.basename(file), "{desc}", "{media_pool}")

manager.cleanup(tmp)
        
        """)

        f.save_generated_script(name)
        print(200)
