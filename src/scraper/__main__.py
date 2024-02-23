from context import src
from context import lib
from src import *
from lib import *


def main():
    pg.verify_cfg()
    v1 = pg.main_menu("Scraper")
    if v1 == 'custom':
        # Make scraper formula
        pass

    if v1 == 'manual':

        inputs = [
            InputPage("Manually Inputting a media file.\nInput absolute path of content to upload:\n(FILE MUST BE VISIBLE TO COMPUTER)").prompt(),
            InputPage("Input the media type.\nAccepted types: 'text', 'audio', 'image', 'video'.").prompt(),
            InputPage("Input a title for the media file:").prompt(),
            InputPage("Input a description for the media file:").prompt(),
            InputPage("Input the associated name of the media pool that this file is related to:").prompt()
        ]

        try:
            db = DbNasConnection()
            db.create_media_file(*inputs)
        except Exception as e:
            raise e
        print("ret value: 200")


if __name__ == '__main__':
    main()

