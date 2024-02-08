from context import lib
from context import src
from lib import *
from src import *

import os

"""
Methods for interacting with central
"""


# --- Account methods ---

def create_account(username, email, password, platform, description):
    # Action for "Create Account"
    try:
        db = DbNasConnection()
        db.create_account(username, email, password, platform, description)
    except Exception as e:
        return e
    return 200


def delete_account(account_id):
    # Action for "Delete Account"
    try:
        db = DbNasConnection()
        db.delete_account(account_id)
    except Exception as e:
        return e
    return 200


def display_account(username):
    # Action for "Display Account"
    try:
        db = DbNasConnection()
        record = db.read_account_by_name(username)
    except Exception as e:
        return e
    return record


# --- media pool methods ---

def create_media_pool(media_pool_name, description):
    try:
        db = DbNasConnection()
        db.create_media_pool(media_pool_name, description)
    except Exception as e:
        return e
    return 200


def delete_media_pool(media_pool_id):
    try:
        db = DbNasConnection()
        db.delete_media_pool(media_pool_id)
    except Exception as e:
        return e
    return 200


def display_media_pool(media_pool_name):
    try:
        db = DbNasConnection()
        record = db.read_media_pool_by_name(media_pool_name)
    except Exception as e:
        return e
    return record


# --- linking methods ---

def link_account_to_media_pool(id_account, id_media_pool):
    # Action for "Link Account to Media Pool"
    try:
        db = DbNasConnection()
        db.create_link_account_to_media_pool(id_account, id_media_pool)
    except Exception as e:
        return e
    return 200


def unlink_account_to_media_pool(id_account, id_media_pool):
    try:
        db = DbNasConnection()
        db.delete_link_account_to_media_pool(id_account, id_media_pool)
    except Exception as e:
        return e
    return 200

# --- creating archiver services ---


def create_archiver_service(service_name, on_cal_list: list):
    """
    Creates an archiver service that archives all file with the to_archive  label
    :param service_name:
    :param on_cal_list:
    :return:
    """

    try:
        # First create the python script
        formula = ManageFormula()
        formula.append_code("db = DbNasConnection()")
        formula.append_code("db.delete_all_archived_media_files()")

        # Save the script
        formula.save_generated_script(service_name)

        # Then create the service
        ManageService().create(service_name, on_cal_list)
    except Exception as e:
        return e
    return 200


def delete_archiver_service(service_name):
    # Action for "Delete Archiver Service"
    try:
        ManageService().delete(service_name)
        ManageFormula().delete_generated_script(service_name)
    except Exception as e:
        return e
    return 200


def display_services():
    # Action for "Display Services"
    try:
        record = ManageService().print_map()
    except Exception as e:
        return e
    return record


"""
MAIN
"""
if __name__ == '__main__':
    print(os.getcwd())
    pg.verify_cfg()

    p1 = PickerPage(["ACCOUNT",
                     "MEDIA POOLS",
                     "LINK ACCOUNT & MEDIA POOL",
                     "MANAGE SERVICE"])

    v1 = p1.prompt()  # This will determine what submenu to navigate to.

    if v1 == 0:  # ACCOUNTS

        p2 = PickerPage(["create account",
                         "delete account",
                         "display account",
                         "display all"])

        v2 = p2.prompt()
        if v2 == 0:  # create account
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

            ret = create_account(*result_list)
            print(f"ret value {ret}")

        if v2 == 1:  # delete account
            acc_id = InputPage("Input account id to delete")
            ret = delete_account(acc_id)
            print(f"ret value {ret}")

        if v2 == 2:  # display account
            acc_name = InputPage("Input account name")
            ret = display_account(acc_name)
            print(f"ret value {ret}")

        if v2 == 3:  # display all accounts
            pass  # TODO

    elif v1 == 1:  # MEDIA POOLS

        p2 = PickerPage(["create media pool",
                         "delete media pool",
                         "display media pool",
                         "display all media pools"])
        v2 = p2.prompt()

        if v2 == 0:  # create media pool
            name = InputPage("Input media pool name").prompt()
            desc = InputPage("Input a description").prompt()
            ret = create_media_pool(name, desc)
            print(f"return value, {ret}")

        if v2 == 1:  # delete media pool
            media_id = InputPage("Input media pool id to delete").prompt()
            ret = delete_media_pool(media_id)
            print(f"return value, {ret}")

        if v2 == 2:  # display media pool
            media_pool_name = InputPage("Input media pool name").prompt()
            ret = display_media_pool(media_pool_name)
            print(f"return value\n {ret}")

        if v2 == 3:  # display all media pools
            pass  # TODO

    elif v1 == 2:  # MANAGE ACCOUNT & MEDIA POOL LINK

        p2 = PickerPage(["link", "unlink"])
        v2 = p2.prompt()

        if v2 == 0:  # link
            acc_id = InputPage("Input account id").prompt()
            pool_id = InputPage("Input media pool id").prompt()
            result = link_account_to_media_pool(acc_id, pool_id)  # Got an infinite loop here
            print(f"return value\n {result}")

        if v2 == 1:  # unlink
            acc_id = InputPage("Input account id").prompt()
            pool_id = InputPage("Input media pool id").prompt()
            result = unlink_account_to_media_pool(acc_id, pool_id)  # And here
            print(f"return value\n {result}")


    elif v1 == 3:  # MANAGE SERVICE

        p2 = PickerPage(["Create Archiver Service",
                         "Delete Archiver Service",
                         "Display Services"])

        v2 = p2.prompt()
        if v2 == 0:  # create archiver service
            prompt_values = pg.start_service()
            ret = create_archiver_service(prompt_values[0], prompt_values[1])
            print(f"return value {ret}")

        if v2 == 1:  # delete archiver service
            name = InputPage("Input service name to delete").prompt()
            ret = delete_archiver_service(name)
            # raise ret
            print(f"return value {ret}")

        if v2 == 2:  # display service
            ret = display_services()
            print(f"return value\n {ret}")


