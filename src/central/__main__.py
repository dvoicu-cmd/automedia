from context import lib
from context import src
from lib import *
from src import *

import os

"""
Methods for interacting with central
"""


def create_account(username, email, password, platform, description):
    # Action for "Create Account"
    db = DbNasConnection()
    db.create_account(username, email, password, platform, description)
    pass


def delete_account(account_id):
    # Action for "Delete Account"
    db = DbNasConnection()
    db.delete_account(account_id)
    pass


def display_account(username):
    # Action for "Display Account"
    db = DbNasConnection()
    record = db.read_account_by_name(username)
    print(record)
    pass


def link_account_to_media_pool():
    # Action for "Link Account to Media Pool"
    pass


def create_archiver_service():
    # Action for "Create Archiver Service"
    pass


def delete_archiver_service():
    # Action for "Delete Archiver Service"
    pass


def start_service():
    # Action for "Start Service"
    pass


def stop_service():
    # Action for "Stop Service"
    pass


def display_services():
    # Action for "Display Services"
    pass




"""
MAIN
"""
if __name__ == '__main__':
    print(os.getcwd())
    pg.verify_cfg()

    p = PickerPage(["Create Account",
                    "Delete Account",
                    "Display Account",
                    "Create Media"
                    "Link Account to Media Pool",
                    "Create Archiver Service",
                    "Delete Archiver Service",
                    "Start Service",
                    "Stop Service",
                    "Display Services"])

    v = p.prompt()
    # Menu options with associated actions
    if v == 0:
        in_list = [
            InputPage("Username"),
            InputPage("Email"),
            InputPage("Password"),
            InputPage("Platform"),
            InputPage("Description")
        ]

        result_list = []
        for page in in_list:
            answer = page.prompt()
            result_list.append(answer)

        create_account(*result_list)

    elif v == 1:
        p = InputPage("Account ID")
        value = p.prompt()
        delete_account(value)

    elif v == 2:
        p = InputPage("Account Name")
        value = p.prompt()
        display_account(value)

    elif v == 3:

        link_account_to_media_pool()
    elif v == 4:
        create_archiver_service()
    elif v == 5:
        delete_archiver_service()
    elif v == 6:
        start_service()
    elif v == 7:
        stop_service()
    elif v == 8:
        display_services()