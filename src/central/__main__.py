from context import lib
from lib import *

def




"""
MAIN
"""
if __name__ == '__main__':
    pages = [PickerPage(["Add Account", "Delete Account", "Add Media_Pool", ]),
             InputPage("Input account name"),
             PickerPage([""])]
    mapping = {'main': 0, 0: 1, 1: 2,}
    c1 = Cli(pages=pages, mapping=mapping)
    c2 = Cli()


    pass

