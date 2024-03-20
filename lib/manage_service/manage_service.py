"""

Note on timers: Timing needs to be done in a specific format
For OnUnitActiveSec:
s -> seconds, min -> minutes, d -> days, w -> weeks, M -> months, y -> years
ex: OnUnitActiveSec=5min activates the script every five minutes
"""

import subprocess
import os
from .service_configurator import ServiceConfigurator
from .timer_map import TimerMap


class ManageService:
    def __init__(self):
        """
        Constructor for ManageService class
        """
        # class that abstractions the writing and loading params in the paths.cfg file
        self.service_config = ServiceConfigurator()
        # class that reads, writes, and deletes the mapping of python files to their execution times
        self.timer_map = TimerMap()

    # --------- Public Methods --------- #

    def create(self, python_file, on_calendar_list):
        """
        Creates a cron service that executes the inputted python script on the given schedule.
        https://crontab.guru/

        Args:
            python_file (str): The string that contains the name of the python file excluding the .py extension in the current directory
            on_calendar_list (list): A list of strings in the appropriate on calendar format. ex: ["*-*-* 21:00:00", "*-*-* 09:00:00"]
        """

        # Load the saved timer map
        self.timer_map.deserialize()

        # Attempt to add the file name as a key
        self.timer_map.new_timer_key(python_file)

        # Add on_calendar_list to the mapping
        self.timer_map.new_exec_time_value(python_file, on_calendar_list)

        # Write the service and timer files
        self.__write_cron_file(python_file, on_calendar_list)

        # Save serialize the timer map
        self.timer_map.serialize()

    def delete(self, python_file):
        """
        Deletes the systemd service and associated files for a python script given that the script it has a service.

        Args:
            python_file (str): The string that contains the name of the python file excluding the .py extension in the current directory
        """
        # Load the saved timer map
        self.timer_map.deserialize()

        # Delete the key on the map
        self.timer_map.delete_timer_key(python_file)

        # Delete files
        self.__delete_cron_file(python_file)

        # Save to pickle file
        self.timer_map.serialize()

    def create_paths_config(self, service_dir_path, python_runtime_path, python_scripts_path):
        """
        Creates a paths.cfg file in the current directory that contains the needed absolute file paths to create services

        Args:
            service_dir_path: The path pointing towards the directory for loading systemd .service and .timer files.
            Typically located on linux machines in /etc/systemd/system
            python_runtime_path: The path that points towards the python binary file. Typically located in /bin/python3
            python_scripts_path: The path that points to the python scripts that you wish to run schedule
        """
        self.service_config.write(service_dir_path, python_runtime_path, python_scripts_path)

    def print_map(self):
        """
        returns the recorded timer map
        """
        # Load map from pickle file
        self.timer_map.deserialize()
        return self.timer_map.json_return()

    # --------- Writing Files --------- #

    def __write_cron_file(self, py_file, on_calendar_list):
        """
        Writes the .timer file given the location found in the paths.cfg file

        Args:
            py_file (str): The string that contains the name of the python file excluding the .py extension in the current directory
            on_calendar_list (list): on_calendar_list (list): A list of strings in the appropriate on calendar format. ex: ["*-*-* 21:00:00", "*-*-* 09:00:00"]

        """
        path_dict = self.service_config.read()

        cmd = f"{path_dict.get('python_runtime_path')} {path_dict.get('python_scripts_path')}/{py_file}.py"

        file_content = "MAILTO=\"\"\n"

        # Append the on calendar elements
        for on_calendar_element in on_calendar_list:
            file_content = f"{file_content}{on_calendar_element} root {cmd}\n"

        with open(f"{path_dict.get('service_dir_path')}/{py_file}_job", 'w') as f:
            f.write(file_content)

    # --------- Deleting Files --------- #

    def __delete_cron_file(self, py_file):
        """
        Deletes the .service file given the location found in the paths.cfg file

        Args:
            py_file (str): The string that contains the name of the python file excluding the .py extension in the current directory
        """

        path_dict = self.service_config.read()
        os.remove(f"{path_dict.get('service_dir_path')}/{py_file}_job")

    # --------- Helper Method --------- #

    def run_py_service(self, py_file):
        """
        Manually runs the py file in a py_services package
        :return:
        """
        service_name = py_file

        paths = self.service_config.read()

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
