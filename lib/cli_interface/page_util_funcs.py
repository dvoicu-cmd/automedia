# Getting the ide to stfu
from lib.central_connector.db_nas_connection import DbNasConnection
from lib.manage_service.manage_service import ManageService
from lib.manage_service.service_configurator import ServiceConfigurator
from lib.manage_formula.manage_formula import ManageFormula
from .input_pages import InputPage
from .picker_pages import PickerPage
import os
import subprocess

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
            InputPage("There is no \"cred.cfg\" file for database. Input host ip:"),
            InputPage("Port"),
            InputPage("User"),
            InputPage("Password"),
            InputPage("Database Name"),
            InputPage("Nas root file location on this machine:")
        ]

        result_list = []
        for page in in_list:
            answer = page.prompt()
            result_list.append(answer)

        cfg_db = DbNasConnection()
        cfg_db.make_connection_config(*result_list)

    if not os.path.exists('paths.cfg'):
        in_list = [
            InputPage("There is no \"paths.cfg\" file for managing services. \n Input the absolute path of the service directory"),
            InputPage("absolute path of the python binary"),
            InputPage("The absolute path of the scripts")
        ]
        paths_list = []
        for page in in_list:
            answer = page.prompt()
            paths_list.append(answer)

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
        page = InputPage("Input an on calendar value to schedule this service\nsystemd timers use the format: {day of the week} {year}-{month}-{day} {hr}:{min}:{sec}.")
        on_cal_list.append(page.prompt())

        # prompt if user wishes to add more on_calendar values
        continue_loop = PickerPage([
            "Add another on calendar time",
            "Save file"
        ])
        result = continue_loop.prompt()
        if result == 1:
            contd = False

    # Call the on manager service method
    return [service_name, on_cal_list]

# Be honest, these two don't actually matter as much
# def stop_service():
#     """
#     Wraps the end service with a cli input
#     """
#     page = InputPage("Input the service to stop")
#     name = page.prompt()
#     ManageService().delete(name)
#     print(f"DELETED SERVICE: {name}")
#
#
# def view_service_map():
#     """
#     prints the dictionary of the service map
#     :return:
#     """
#     print("SERVICE MAP: \n")
#     print(ManageService().print_map())


def main_menu(node_name):
    page = PickerPage(
        [
            f"Create {node_name} formula",
            f"Delete {node_name} formula",
            f"Display Service Map",
            f"Display All formulas"
            f"Start Service",
            f"Stop Service"
        ])

    v = page.prompt()
    if v == 0:  # Create formula
        return 'custom'  # Do something custom in the __main__.py

    if v == 1:  # Delete a formula
        value = InputPage("Input the formula to delete").prompt()
        try:
            ManageFormula().delete_generated_script(value)
        except Exception as e:
            raise e

    if v == 2:  # Display map
        try:
            print(ManageService().print_map())
        except Exception as e:
            raise e

    if v == 3:  # Display all formulas
        try:
            print(f"All service files: \n {ManageFormula().print_script_names()}")
        except Exception as e:
            raise e

    if v == 4:  # Start Service
        try:
            out = start_service()
            ManageService().create(out[0], out[1])
        except Exception as e:
            raise e

    if v == 5:  # Stop service
        try:
            value = InputPage("Input the name of the service you wish to stop").prompt()
            ManageService().delete(value)
        except Exception as e:
            raise e
