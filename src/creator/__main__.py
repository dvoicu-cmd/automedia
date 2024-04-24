from context import src
from context import lib
from src import *
from lib import *


"""
Wrapper functions
"""


def main():
    pg.verify_cfg()
    v1 = pg.main_menu("Creator")
    if v1 == 'custom':
        # CUSTOM CREATOR FORMULA CREATION
        v2 = PickerPage(["Text Story", "Cycle Images Story"]).prompt("Select a formula to use")
        if v2 == 0:
            CreatorFormulas().generic_text_story()
        if v2 == 1:
            CreatorFormulas().cycling_images_story()

    # end of custom

    if v1 == 'manual':
        inputs = [
            InputPage("Manually uploading content file:\n Input the absolute file location of the contents you wish to upload").prompt(),
            InputPage("Input the title of the content:").prompt(),
            InputPage("Input a description for the content file(s):").prompt(),
            InputPage("Input the associated name of the account that these contents are related to:").prompt()
        ]
        try:
            db = DbNasConnection()
            db.create_content(*inputs)
        except Exception as e:
            raise e
        print(200)



if __name__ == '__main__':
    main()

