from context import src
from context import lib
from src import *
from lib import *

if __name__ == '__main__':
    pg.verify_cfg()
    v1 = pg.main_menu("scraper")
    if v1 == 'custom':

        # CUSTOM SCRAPER FORMULA CREATION
        v2 = PickerPage(['Make Scraper Formula', 'Manually Upload Content to Media Pool']).prompt()
        if v2 == 0:
            # MAKE SCRAPER FORMULA
            pass
        if v2 == 1:
            pool_parent = InputPage("Input Media pool to upload to:").prompt()
            content = InputPage("Input absolute path to file you wish to upload:").prompt()

            content_types = ['text', 'audio', 'image', 'video']
            index = PickerPage(['text', 'audio', 'image', 'video']).prompt()

            title = InputPage("Input a title").prompt()
            desc = InputPage("Input a description").prompt()

            DbNasConnection().create_media_file(content, content_types[index], title, desc, pool_parent)
            print(200)

