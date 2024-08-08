from context import src
from context import lib
from src import *
from lib import *


def main():
    pg.verify_cfg()
    v1 = pg.main_menu("Creator")
    if v1 == 'custom':
        # CUSTOM CREATOR FORMULA CREATION
        v2 = PickerPage(["Text Story",
                         "Cycle Images Story",
                         "Cycle Image Story Shorts",
                         "Back"
                         ]).prompt("Select a formula to use")
        try:
            if v2 == 0:
                CreatorFormulas().generic_text_story()
                DisplayPage().prompt("Created text story formula.")
            if v2 == 1:
                CreatorFormulas().cycling_images_story()
                DisplayPage().prompt("Created cycling image formula.")
            if v2 == 2:
                CreatorFormulas().cycling_images_story_shorts()
                DisplayPage().prompt("Created cycling image story shorts formula.")
            if v2 == 3:
                pass
        except Exception as e:
            if isinstance(e, InputCancelled):
                InputPage("").print_cancelled_input()
            else:
                DisplayPage().prompt(pg.str_exception(e))

    # end of custom

    if v1 == 'manual':

        v2 = PickerPage(["Input Content File",
                         "Execute Service",
                         "Back"]).prompt("Manual Creator Functions.\nSelect an option.")

        if v2 == 0:  # Input content file
            try:
                inputs = [
                    InputPage("Manually uploading content file:\n Input the absolute file location of the contents you wish to upload").prompt(),
                    InputPage("Input the title of the content:").prompt(),
                    InputPage("Input a description for the content file(s):").prompt(),
                    InputPage("Input the associated name of the account that these contents are related to:").prompt()
                ]
                db = DbNasConnection()
                db.create_content(*inputs)
            except Exception as e:
                if isinstance(e, InputCancelled):
                    InputPage("").print_cancelled_input()
                else:
                    DisplayPage.prompt(pg.str_exception(e))

        if v2 == 1:  #
            pg.manual_execution()

        if v2 == 2:
            pass



if __name__ == '__main__':
    main()

