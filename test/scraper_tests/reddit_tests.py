from context import src
from context import lib
from src.scraper.platform_strategies.reddit_web import RedditScrape
from lib.manage_directory_structure.scraper_dir_manager import ScraperDirManager
from lib.central_connector.db_nas_connection import DbNasConnection
import pdb


def main():
    manager = ScraperDirManager()
    # db_nas = DbNasConnection()
    tmp = manager.create_tmp_dir()

    rd = RedditScrape()
    output = rd.scrape("AmItheAsshole", "hot", "text", 1, 4)

    manager.dl_list_of_text(output, 'AM_I_THE_ASSHOLE', tmp)

    entries = manager.select_dir(tmp)

    rd.quit()

    pdb.set_trace()

    manager.cleanup(tmp)

    pass



main()
