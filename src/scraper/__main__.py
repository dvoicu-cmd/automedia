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
        # CUSTOM SCRAPER FORMULA CREATION
        v2 = PickerPage(["Reddit Scrape", "Ai Text Prompt", "Ai Text and Images"]).prompt("Select a formula to use")
        try:
            if v2 == 0:
                ScraperFormulas().reddit_scrape()
            if v2 == 1:
                ScraperFormulas().open_ai_text()
            if v2 == 2:
                ScraperFormulas().open_ai_text_and_img()
        except Exception as e:
            if isinstance(e, InputCancelled):
                InputPage("").print_cancelled_input()
            else:
                DisplayPage().prompt(pg.str_exception(e))

    if v1 == 'manual':

        try:
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

            DisplayPage().prompt(f"Successfully inputted media.")

        except Exception as e:
            if isinstance(e, InputCancelled):
                InputPage("").print_cancelled_input()
            else:
                DisplayPage().prompt(pg.str_exception(e))


if __name__ == '__main__':
    main()

