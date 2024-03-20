# Getting the ide to stfu
from lib.central_connector.db_nas_connection import DbNasConnection
from lib.manage_service.manage_service import ManageService
from lib.manage_formula.manage_formula import ManageFormula
from .input_pages import InputPage
from .picker_pages import PickerPage
import os

"""
General wrapper functions for the cli user input
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
            InputPage("Input the root file mount location for the nas on this machine: \n"
                      "Typically the default location is /mnt")
        ]

        result_list = []
        for page in in_list:
            answer = page.prompt()
            result_list.append(answer)

        cfg_db = DbNasConnection()
        cfg_db.make_connection_config(*result_list)

    if not os.path.exists('paths.cfg'):
        service_path = InputPage("There is no configuration set up for managing services. \n"
                                 "Input the absolute path of the cron system directory. \n"
                                 "Typically on debian systems this would be: /etc/cron.d").prompt()

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
    :return:
    """
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


def main_menu(node_name):
    page = PickerPage(
        [
            f"Create {node_name} Formula",
            f"Delete {node_name} Formula",
            f"Display All Formulas",
            f"Display Service Map",
            f"Start Service",
            f"Stop Service",
            f"Manual Action"
        ])

    v = page.prompt(f"{node_name} Menu \nselect an option:")
    if v == 0:  # Create formula
        return 'custom'  # Do something custom in the __main__.py file

    if v == 1:  # Delete a formula
        value = InputPage("Input the name of the formula to delete").prompt()
        try:
            ManageFormula().delete_generated_script(value)
        except Exception as e:
            raise e

    if v == 2:  # Display all formulas
        InputPage.clear()
        try:
            print(f"All files in py_services: \n {ManageFormula().print_script_names()}")
        except Exception as e:
            raise e

    if v == 3:  # Display Service Map
        InputPage.clear()
        try:
            print(ManageService().print_map())
        except Exception as e:
            raise e

    if v == 4:  # Start Service
        InputPage.clear()
        try:
            out = start_service()
            ManageService().create(out[0], out[1])
        except Exception as e:
            raise e

    if v == 5:  # Stop service
        InputPage.clear()
        try:
            value = InputPage("Input the name of the service you wish to stop").prompt()
            ManageService().delete(value)
        except Exception as e:
            raise e

    if v == 6:  # Manual action
        return 'manual'  # manual action to be done in __main__.py
