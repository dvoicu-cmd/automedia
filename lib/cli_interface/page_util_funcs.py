# Getting the ide to stfu
from lib.central_connector.db_nas_connection import DbNasConnection
from lib.manage_service.manage_service import ManageService
from lib.manage_formula.manage_formula import ManageFormula
from lib.cli_interface.page.sigint_handling.input_cancelled import InputCancelled
from .page.input_pages import InputPage
from .page.picker_pages import PickerPage
from .page.display_page import DisplayPage
import traceback
import os
import re

"""
General wrapper and helper functions for the cli user input
"""


def verify_cfg():
    """
    A function that prompts pages in case the cred.cfg and paths.cfg file is not present.
    :return:
    """
    if not os.path.exists('cred.cfg'):
        in_list = [
            InputPage("The credentials for the database have not been setup. \n"
                      "Input the host ip of the database:"),
            InputPage("Input the sql port of the database server:"),
            InputPage("Input the database username this node will use:"),
            InputPage("Input the password for the user:"),
            InputPage("Input the name of the database:"),
            # yeah, you don't need this as the make file sets the files to /mnt
            # InputPage("Input the root file mount location for the nas on this machine: \n"
            #           "Typically the default location is /mnt")
        ]

        result_list = []
        for page in in_list:
            answer = str(page.prompt())
            result_list.append(answer)

        result_list.append("/mnt")

        cfg_db = DbNasConnection()
        cfg_db.make_connection_config(*result_list)

    if not os.path.exists('paths.cfg'):
        # eh, this ain't quite needed to prompt for cron's location.
        # service_path = InputPage("There is no configuration set up for managing services. \n"
        #                          "Input the absolute path of the cron system directory. \n"
        #                          "Typically on debian systems this would be: /etc/cron.d").prompt()
        service_path = "/etc/cron.d"

        cwd = os.getcwd()  # save current working directory
        # assuming at, py_services
        os.chdir('..')  # cd to specific node type package
        os.chdir('..')  # cd to src
        os.chdir('..')  # cd to automedia root
        venv_path = os.getcwd()+'/.venv/automedia_venv/bin/python3'  # get the venv path

        os.chdir(cwd)  # change dir back

        paths_list = [
            service_path,  # append the service dir
            venv_path,  # append the default expected location of the python virtual environment
            cwd  # Input the current directory to read from the python scripts in py_services
        ]

        # Create paths.cfg file
        service = ManageService()
        service.create_paths_config(*paths_list)


#  ------------ service functions ------------

def start_service():
    """
    grabs the cli input for starting a service
    :return: An array size 2. The first item is a string with the name of the service and second item is the list of oncalendar values
    :raises: InputCancelled exception when an input page detects a sigint. Up to caller to handle it.
    """
    try:
        page = InputPage("Input the service you wish to start. (Exclude the .py extension)")
        service_name = page.prompt()

        # Loop to add on_calendar values
        contd = True
        on_cal_list = []
        while contd:
            page = InputPage("Input cron interval to schedule this service. \n"
                             "Cron timers use the format: {minute} {hour} {day #} {month} {day of the week}\n"
                             "*	--> any value \n"
                             ", --> value list separator\n"
                             "- --> range of values\n"
                             "/	--> step values.")
            on_cal_list.append(page.prompt())

            # prompt if user wishes to add more on_calendar values
            continue_loop = PickerPage([
                "Add another cron time",
                "Save file"
            ])
            result = continue_loop.prompt()
            if result == 1:
                contd = False

        # Call the on manager service method
        return [service_name, on_cal_list]
    except InputCancelled as e:
        raise e


def main_menu(node_name):
    """
    Shared main menu prompt among creator, publisher, and scraper.
    :param node_name:
    :return:
    """
    page = PickerPage(
        [
            f"Create {node_name} Formula",
            f"Delete {node_name} Formula",
            f"Display All Formulas",
            f"Display Service Map",
            f"Start Service",
            f"Stop Service",
            f"Manual Action",
            f"Quit"
        ])

    v = page.prompt(f"{node_name} Menu \nselect an option:")
    if v == 0:  # Create formula
        return 'custom'  # Do something custom in the __main__.py file

    if v == 1:  # Delete a formula
        try:
            value = InputPage("Input the name of the formula to delete").prompt()
        except InputCancelled:
            InputPage("").print_cancelled_input()
            return

        try:
            ManageFormula().delete_generated_script(value)
            DisplayPage().prompt(f"Successfully deleted formula: {value}")
        except Exception as e:
            DisplayPage().prompt(str_exception(e))


    if v == 2:  # Display all formulas
        InputPage.clear()
        try:
            # Stupid. Filtering py_services to just display the py files that where created by the formula class.
            # Fix: Find all files with .py, exclude key files. like context.py then chop the .py part and display.
            ls = ManageFormula().print_script_names()
            srt_pattern = re.compile(r'srt_tmp_[A-Za-z0-9]{5}$')
            tmp_video = re.compile(r'videoTEMP_[A-Za-z0-9]{3}_[A-Za-z0-9]{3}_[A-Za-z0-9]{3}.mp4')
            ls_to_filter = ['cache', 'log', 'output', '__pycache__', 'timer_map.pickle', '__init__.py', 'context.py', 'cred.cfg', 'paths.cfg']
            filtered_list = [item for item in ls if item not in ls_to_filter or srt_pattern.match(item) or tmp_video.match(item)]  # Filter out the list

            DisplayPage().prompt(f"All formulas: \n\n {filtered_list}")
        except Exception as e:
            DisplayPage().prompt(str_exception(e))

    if v == 3:  # Display Service Map
        InputPage.clear()
        try:
            DisplayPage().prompt(f"Displaying all services: \n\n {ManageService().print_map()}")
        except Exception as e:
            DisplayPage().prompt(str_exception(e))

    if v == 4:  # Start Service
        InputPage.clear()
        try:
            out = start_service()
            ManageService().create(out[0], out[1])
            DisplayPage().prompt(f"Successfully started service: {out[0]}")
        except Exception as e:
            if isinstance(e, InputCancelled):
                InputPage("").print_cancelled_input()
            else:
                DisplayPage().prompt(str_exception(e))

    if v == 5:  # Stop service
        InputPage.clear()
        try:
            value = InputPage("Input the name of the service you wish to stop").prompt()
            ManageService().delete(value)
            DisplayPage().prompt(f"Successfully stopped the service: {value}")
        except Exception as e:
            DisplayPage().prompt(str_exception(e))

    if v == 6:  # Manual action
        return 'manual'  # manual action to be done in __main__.py

    if v == 7:  # Terminate Program
        InputPage.clear()
        quit("Bye")


def str_exception(ret):
    """
    Gets an exception object into a string stack strace
    :param ret:
    :return:
    """
    tb_exception = traceback.TracebackException.from_exception(ret)
    traceback_str = ''.join(tb_exception.format())
    return traceback_str
