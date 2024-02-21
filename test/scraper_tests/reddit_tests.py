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
    output = rd.scrape("memes", "new", "image", 2, 5)

    print(output)

    manager.dl_list_of_links(output, 'image', 'reddit_memes', tmp)


    manager.cleanup(tmp)

    pass



main()
