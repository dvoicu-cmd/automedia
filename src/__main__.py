import configparser
import sys
import os

from src.creator.__main__ import main as creator_main
from src.scraper.__main__ import main as scraper_main
from src.publisher.__main__ import main as publisher_main
from src.central.__main__ import main as central_main


def main():
    # Read configuration
    config = configparser.ConfigParser()
    file = config.read('config.ini')
    if len(file) == 0:
        raise FileExistsError('No config.ini file at project root')
    module = config['NODE_TYPE']['type']

    # Import and run the selected submodule
    try:
        wd = os.getcwd()
        if module == 'central':
            os.chdir(f'{wd}/central/py_services')
            print(os.getcwd())
            central_main()
        elif module == 'creator':
            os.chdir(f'{wd}/creator/py_services')
            creator_main()
        elif module == 'publisher':
            os.chdir(f'{wd}/publisher/py_services')
            publisher_main()
        elif module == 'scraper':
            os.chdir(f'{wd}/scraper/py_services')
            scraper_main()
        else:
            raise ModuleNotFoundError
    except ModuleNotFoundError:
        print(f"Error: Submodule '{module}' not found.")
        sys.exit(1)


if __name__ == "__main__":
    main()
