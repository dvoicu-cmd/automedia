import configparser
import sys
import os

from src.creator.__main__ import main as creator_main
from src.scraper.__main__ import main as scraper_main
from src.publisher.__main__ import main as publisher_main
from src.central.__main__ import main as central_main

from lib.cli_interface.page.picker_pages import PickerPage


def main():
    # Read configuration
    config = configparser.ConfigParser()
    file = config.read('config.ini')
    if len(file) == 0:
        a = PickerPage(['central', 'creator', 'publisher', 'scraper']).prompt("**** automedia ****\n\nThe node type has not been configured. \nSelect what node type this machine is:")
        with open('config.ini', 'w') as configfile:
            if a == 0:  # central
                config['NODE_TYPE'] = {'type': 'central'}
                config.write(configfile)
            elif a == 1:  # creator
                config['NODE_TYPE'] = {'type': 'creator'}
                config.write(configfile)
            elif a == 2:  # publisher
                config['NODE_TYPE'] = {'type': 'publisher'}
                config.write(configfile)
            elif a == 3:  # scraper
                config['NODE_TYPE'] = {'type': 'scraper'}
                config.write(configfile)
            else:
                raise FileNotFoundError('Invalid config.ini file choice. Somehow...')
        # Re-read the file now
        config.read('config.ini')

    module = config['NODE_TYPE']['type']

    # Import and run the selected submodule
    try:
        wd = os.getcwd()
        if module == 'central':
            os.chdir(f'{wd}/central/py_services')
            while True:  # Main Prompt for central
                central_main()
        elif module == 'creator':
            os.chdir(f'{wd}/creator/py_services')
            while True:  # Main Prompt for creator
                creator_main()
        elif module == 'publisher':
            os.chdir(f'{wd}/publisher/py_services')
            while True:  # Main Prompt for publisher
                publisher_main()
        elif module == 'scraper':
            os.chdir(f'{wd}/scraper/py_services')
            while True:  # Main Prompt for scraper
                scraper_main()
        else:
            raise ModuleNotFoundError
    except ModuleNotFoundError:
        print(f"Error: Submodule '{module}' not found.")
        sys.exit(1)


if __name__ == "__main__":
    main()
