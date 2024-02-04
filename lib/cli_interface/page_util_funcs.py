# Getting the ide to stfu
from lib.central_connector.db_nas_connection import DbNasConnection
from lib.manage_service.manage_service import ManageService
from lib.manage_service.service_configurator import ServiceConfigurator
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
    Wraps the start service with a cli input
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
            "Add another on calendar time"
            "Save file"
        ])
        result = continue_loop.prompt()
        if result == 1:
            contd = False

    # Call the on manager service method
    ManageService().create(service_name, on_cal_list)
    print(f"CREATED SERVICE FOR: {service_name}")


def stop_service():
    """
    Wraps the end service with a cli input
    """
    page = InputPage("Input the service to stop")
    name = page.prompt()
    ManageService().delete(name)
    print(f"DELETED SERVICE: {name}")


def view_service_map():
    """
    prints the dictionary of the service map
    :return:
    """
    print("SERVICE MAP: \n")
    print(ManageService().print_map())



def run_py_service():
    """
    Manually runs the py file in a py_services package
    :return:
    """
    page = InputPage("Input the name of the py_service file you wish to run")
    service_name = page.prompt()

    paths = ServiceConfigurator().read()

    # Get the python run time used by service files
    python_runtime = paths.get('python_runtime_path')

    # Get the specific script file to run
    service_path = paths.get('python_scripts_path')
    specific_service_script = service_path + "/" + service_name + ".py"

    try:
        subprocess.run([python_runtime, specific_service_script], check=True)
        print("Script executed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error running the script: {e}")


#  ------------ formula functions ------------

