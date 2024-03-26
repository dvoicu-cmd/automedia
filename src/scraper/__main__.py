import os
import copy
from context import src
from context import lib
from src import *
from lib import *


def main():
    pg.verify_cfg()
    v1 = pg.main_menu("Scraper")
    if v1 == 'custom':
        # Make scraper formula

        # This is a strategy for reddit scrapes

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

    if v1 == 'manual':

        path_val = InputPage("Manually Inputting a media file.\nInput absolute path of the content to upload:\n(FILE MUST BE VISIBLE TO COMPUTER)").prompt()
        manager = ScraperDirManager()

        dir_read = False
        if os.path.isdir(path_val):
            v = PickerPage(["Yes", "No"]).prompt("You have entered a directory for a path.\nDo you wish to save all the contents in the directory into one media pool?")
            if v == 0:
                dir_read = True
            elif v == 1:
                list_files_contents = manager.select_dir(path_val)
                str_output = ''
                for path in list_files_contents:
                    str_output = f"{str_output}{os.path.basename(path)}\n"
                specific_file = InputPage(f"{str_output}\n Above is the directories contents. \n Input which file you wish to insert").prompt()
                path_val = f"{path_val}/{specific_file}"

        inputs = [
            InputPage("Input the media type.\nAccepted types: 'text', 'audio', 'image', 'video'.").prompt(),
            InputPage("Input a title for the media file:").prompt(),
            InputPage("Input a description for the media file:").prompt(),
            InputPage("Input the associated name of the media pool that this file is related to:").prompt()
        ]

        try:
            db = DbNasConnection()

            if dir_read:  # Mass upload implementation
                list_files_contents = manager.select_dir(path_val)
                for file_path in list_files_contents:
                    inputs_copy = copy.deepcopy(inputs)
                    inputs_copy.insert(0, file_path)
                    db.create_media_file(*inputs_copy)
            else:  # Singular upload implementation
                inputs.insert(0, path_val)
                db.create_media_file(*inputs)
        except Exception as e:
            raise e
        print("ret value: 200")


if __name__ == '__main__':
    main()

