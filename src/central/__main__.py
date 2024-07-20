from context import lib
from context import src
from lib import *
from src import *
import traceback

import os
from pyotp import TOTP

"""
Methods for interacting with central
"""


def main():
    pg.verify_cfg()
    p1 = PickerPage(["Account",
                     "Media Pools",
                     "Manage Archival Service",
                     "Quit"
                     ])

    v1 = p1.prompt("Central Node: Pick a menu. \n(use the up or down arrow keys)")  # This will determine what submenu to navigate to.

    if v1 == 0:  # ACCOUNTS

        p2 = PickerPage(["Create Account",
                         "Delete Account",
                         "Display specific account record via username",
                         "Display all accounts",
                         "Display totp now code for account",
                         "Back"
                         ])

        v2 = p2.prompt("Select what to do with Accounts:")
        if v2 == 0:  # create account
            in_list = [
                InputPage("Input details on the new entry:\nAccount Username:"),
                InputPage("Account's Associated Email:"),
                InputPage("Account's Password:"),
                InputPage("Account Platform: \n(accepted values: 'tiktok', 'yt_shorts', 'instagram_reels', 'yt_videos', 'other')"),
                InputPage("Input the 32-bit hash for the account's two factor authentication. \n(Leave blank if not applicable)"),
                InputPage("Input a description describing the account's details:")
            ]

            result_list = []
            # Check for cancels
            try:
                for page in in_list:
                    answer = page.prompt()
                    result_list.append(answer)
            except InputCancelled:  # If at any point user sends a sigint signal,
                InputPage("").print_cancelled_input()
                return   # Break out and re-prompt the page.

            # Execute specific function
            ret = create_account(*result_list)

            # Check if the execution was okay.
            if isinstance(ret, BaseException):
                DisplayPage().prompt(pg.str_exception(ret))  # Display what is wrong if something is wrong
            else:
                if ret == 200:  # Else display a success message
                    DisplayPage().prompt("Successfully created account record")
                else:
                    DisplayPage().prompt(str(ret))  # Extra case just in case something is wrong
            # Rest of the pages follow a similar idea:
            # 1) If there are input pages, check for cancel signals
            # 2) Verify that return value is or is not an error, then display appropriate messaging.

        if v2 == 1:  # delete account
            try:
                acc_id = InputPage("Input account id to delete:")
                inputted_id = acc_id.prompt()
            except InputCancelled:
                InputPage("").print_cancelled_input()
                return

            InputPage.clear()
            print("Querying database...")
            ret = delete_account(inputted_id)

            if isinstance(ret, BaseException):
                DisplayPage().prompt(pg.str_exception(ret))
            else:
                if ret == 200:
                    DisplayPage().prompt("Successfully deleted account record")
                else:
                    DisplayPage().prompt(str(ret))

        if v2 == 2:  # display account
            try:
                acc_name = InputPage("Input account name:")
                name = acc_name.prompt()
            except InputCancelled:
                InputPage("").print_cancelled_input()
                return

            InputPage.clear()
            print("Querying database...")
            ret = display_account(name)

            if isinstance(ret, BaseException):
                DisplayPage().prompt(pg.str_exception(ret))
            else:
                DisplayPage().prompt(f"Displaying Account: \n\n {ret}")

        if v2 == 3:  # display all accounts
            InputPage.clear()
            print("Querying database...")
            ret = display_all_accounts_names()
            if isinstance(ret, BaseException):
                DisplayPage().prompt(pg.str_exception(ret))
            else:
                DisplayPage().prompt(f"Displaying All Accounts: \n\n {ret}")

        if v2 == 4:  # totp now
            try:
                acc_id = InputPage("Input the account id:")
                ret = totp_for_account(acc_id.prompt())
            except InputCancelled:
                InputPage("").print_cancelled_input()
                return

            if isinstance(ret, BaseException):
                DisplayPage().prompt(pg.str_exception(ret))
            else:
                DisplayPage().prompt(f"totp code: {ret}")

        if v2 == 5:  # Back
            pass  # Ignore everything and let __main__ reprompt


    elif v1 == 1:  # MEDIA POOLS

        p2 = PickerPage(["Create Media Pool",
                         "Delete Media Pool",
                         "Display specific Media Pool record via name",
                         "Display all Media Pools",
                         "Back"])

        v2 = p2.prompt("Select what to do with Media Pools:")

        if v2 == 0:  # create media pool
            try:
                name = InputPage("Input the media pool name").prompt()
                desc = InputPage("Input a description").prompt()
            except InputCancelled:
                InputPage("").print_cancelled_input()
                return

            InputPage.clear()
            print("Querying database...")
            ret = create_media_pool(name, desc)

            if isinstance(ret, BaseException):
                DisplayPage().prompt(pg.str_exception(ret))
            else:
                if ret == 200:
                    DisplayPage().prompt(f"Successfully created media pool {name}")
                else:
                    DisplayPage().prompt(ret)

        if v2 == 1:  # delete media pool
            try:
                media_id = InputPage("Input media pool id to delete").prompt()
            except InputCancelled:
                InputPage("").print_cancelled_input()
                return

            InputPage.clear()
            print("Querying database...")
            ret = delete_media_pool(media_id)

            if isinstance(ret, BaseException):
                DisplayPage().prompt(pg.str_exception(ret))
            else:
                if ret == 200:
                    DisplayPage().prompt(f"Successfully deleted media pool")
                else:
                    DisplayPage().prompt(ret)

        if v2 == 2:  # display media pool
            try:
                media_pool_name = InputPage("Input media pool name").prompt()
            except InputCancelled:
                InputPage("").print_cancelled_input()
                return

            InputPage.clear()
            set_watch_signal()
            print("Querying database...")
            ret = display_media_pool(media_pool_name)


            if isinstance(ret, BaseException):
                DisplayPage().prompt(pg.str_exception(ret))
            else:
                DisplayPage().prompt(f"Displaying media pool: \n\n {ret}")

        if v2 == 3:  # display all media pools
            InputPage.clear()
            print("Querying database...")
            ret = display_all_media_pool_names()

            if isinstance(ret, BaseException):
                DisplayPage().prompt(pg.str_exception(ret))
            else:
                DisplayPage().prompt(f"Displaying all media pools: \n\n {ret}")

        if v2 == 4:  # Back
            pass  # Ignore everything, reprompt

    elif v1 == 2:  # MANAGE SERVICE

        p2 = PickerPage(["Create Archiver Service",
                         "Delete Archiver Service",
                         "Display Services",
                         "Manually Archive",
                         "Back"])

        v2 = p2.prompt("Select an action:")


        if v2 == 0:  # create archiver service
            InputPage.clear()
            try:
                prompt_values = pg.start_service()
            except InputCancelled:
                InputPage("").print_cancelled_input()
                return

            ret = create_archiver_service(prompt_values[0], prompt_values[1])
            if isinstance(ret, BaseException):
                DisplayPage().prompt(pg.str_exception(ret))
            else:
                if ret == 200:
                    DisplayPage().prompt(f"Successfully created archiver service.")
                else:
                    DisplayPage().prompt(ret)

        if v2 == 1:  # delete archiver service
            try:
                name = InputPage("Input service name to delete:").prompt()
            except InputCancelled:
                InputPage("").print_cancelled_input()
                return

            ret = delete_archiver_service(name)
            if isinstance(ret, BaseException):
                DisplayPage().prompt(pg.str_exception(ret))
            else:
                if ret == 200:
                    DisplayPage().prompt(f"Successfully deleted archiver service.")
                else:
                    DisplayPage().prompt(ret)

        if v2 == 2:  # display service
            InputPage.clear()
            ret = display_services()
            if isinstance(ret, BaseException):
                DisplayPage().prompt(pg.str_exception(ret))
            else:
                DisplayPage().prompt(f"Displaying all services: \n\n {ret}")

        if v2 == 3:  # manually archive
            InputPage.clear()
            p3 = PickerPage([
                "Media_Pool Files",
                "Account Content Files",
                "Back"
            ])

            v3 = p3.prompt("Select what to immediately archive:")
            if v3 == 0:  # Media pools
                InputPage.clear()
                print("Archiving media pools...")
                try:
                    DbNasConnection().delete_all_archived_media_files()
                    DisplayPage().prompt("Successfully archived media files")
                except Exception as e:
                    DisplayPage().prompt(pg.str_exception(e))
            elif v3 == 1:  # Accounts
                InputPage.clear()
                print("Archiving account videos...")
                try:
                    DbNasConnection().delete_all_archived_content_files()
                    DisplayPage().prompt("Successfully archived account files")
                except Exception as e:
                    DisplayPage().prompt(pg.str_exception(e))
            elif v3 == 2:  # Back
                pass

        if v2 == 4:  # Back
            pass  # Reprompt

    elif v1 == 3:  # QUIT
        InputPage.clear()
        quit("Bye")


# --- Account Helper Methods ---


def create_account(username, email, password, platform, hash2fa, description):
    # Action for "Create Account"
    try:
        db = DbNasConnection()
        db.create_account(username, email, password, platform, hash2fa, description)
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
        formula.append_code("db.delete_all_archived_content_files()")

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


def display_all_accounts_names():
    """
    Reads the list of all the account names
    :return:
    """
    try:
        str_output = ""
        records = DbNasConnection().read_all_accounts()
        for record in records:
            str_output = f"{str_output}{record}\n"
    except Exception as e:
        return e
    return str_output


def display_all_media_pool_names():
    try:
        str_output = ""
        records = DbNasConnection().read_all_media_pools()
        for record in records:
            str_output = f"{str_output}{record}\n"
    except Exception as e:
        return e
    return str_output


def accounts_linked_media_pools(acc_id: int):
    try:
        str_output = ""
        records = DbNasConnection().read_media_pools_of_account(acc_id)
        for record in records:
            str_output = f"{record}\n"
    except Exception as e:
        return e
    return str_output


def totp_for_account(acc_id: int):
    try:
        db = DbNasConnection()
        record = db.read_account_by_id(acc_id)
        hash2fa = record[4]
        tp = TOTP(hash2fa)
        return tp.now()
    except Exception as e:
        return e


"""
MAIN
"""
if __name__ == '__main__':
    main()


