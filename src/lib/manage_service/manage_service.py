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
        Constructor
        Args:
            python_file (str): The file name of the python script that will be run as a service
        """
        self.service_config = ServiceConfigurator()
        self.timer_map = TimerMap()

    def create(self, python_file, on_calendar_list):
        # Load the saved timer map
        self.timer_map.deserialize()

        # Attempt to add the file name as a key
        self.timer_map.new_timer_key(python_file)

        # Add on_calendar_list to the mapping
        self.timer_map.new_exec_times(python_file, on_calendar_list)

        # If the exec times are empty after adding
        exec_times = self.timer_map.get_exec_times(python_file)
        if exec_times is None:
            raise ValueError(f"The provided list: {on_calendar_list} conflicts with all the currently scheduled timers")

        # Write the service file
        self.__write_service_file(python_file)

        # Write the timer file
        self.__write_timer_file(python_file, exec_times)

        # Activate the service with subsystem
        self.__activate_service(python_file)

        # Save serialize the timer map
        return

    def delete(self, python_file):
        # Load the saved timer map

        # Identify service file and timer file

        # Stop services with subsystem

        # Delete file

        return

    def create_paths_config(self, service_dir_path, python_runtime_path, python_scripts_path):
        """

        :param service_dir_path:
        :param python_runtime_path:
        :param python_scripts_path:
        :return:
        """
        self.service_config.write(service_dir_path, python_runtime_path, python_scripts_path)

    def __activate_service(self, py_file):
        """
        Activates the service on the host computer
        :return:
        """
        # Enable the service file

        # Enable the timer file

        # Then start the timer file

        return

    def __stop_service(self, py_file):
        """

        :return:
        """
        # Stop the timer file

        # Disable the timer file

        # Disable the service file


        return

    def __write_service_file(self, py_file):
        """
        Writes the .service file at the specified location
        :return:
        """
        path_dict = self.service_config.read()

        file_content = (f"[Unit]\n"
                        f"Description=''\n"
                        f"After=multi-user.target\n"
                        f"Conflicts=getty@tty1.service\n"
                        f"Wants={py_file}.timer\n"
                        f"\n"
                        f"[Service]\n"
                        f"Type=simple\n"
                        f"User=root\n"
                        f"ExecStart={path_dict.get('python_runtime_path')} {path_dict.get('python_scripts_path')}/{py_file}.py\n"
                        f"WorkingDirectory={path_dict.get('python_scripts_path')}\n"
                        f"KillMode=process\n"
                        f"\n"
                        f"[Install]\n"
                        f"WantedBy=multi-user.target")

        # write file in service directory
        with open(f"{path_dict.get('service_dir_path')}/{py_file}.service", 'w') as f:
            f.write(file_content)

    def __write_timer_file(self, py_file, on_calendar_list):
        """
        Writes the .timer file at the specified location
        :return:
        """
        path_dict = self.service_config.read()

        file_content = (f"[Unit]\n"
                        f"Description=''\n"
                        f"Requires{py_file}.service\n"
                        f"\n"
                        f"[Timer]\n"
                        f"Unit={py_file}.service")

        # Append the on calendar elements
        for on_calendar_element in on_calendar_list:
            file_content = f"{file_content}\nOnCalendar={on_calendar_element}\n"

        # Add remaining items to file
        file_content = (f"{file_content}"
                        f"[Install]\n"
                        f"WantedBy=timers.target")

        with open(f"{path_dict.get('service_dir_path')}/{py_file}.timer", 'w') as f:
            f.write(file_content)

    def __delete_service_file(self, py_file):
        path_dict = self.service_config.read()
        os.remove(f"{path_dict.get('service_dir_path')}/{py_file}.service")

    def __delete_timer_file(self, py_file):
        path_dict = self.service_config.read()
        os.remove(f"{path_dict.get('service_dir_path')}/{py_file}.timer")


"""
----- This is the format of the service file ----

[Unit]
Description={description_service}
After=multi-user.target
Conflicts=getty@tty1.service
Wants={service_name}.timer

# Specify the file paths below
[Service]
Type=simple
User=root
ExecStart=/{path of python3} /{file path of main.py}
WorkingDirectory=/{repository working directory file path}
KillMode=process

[Install]
WantedBy=multi-user.target


---- This is the format of the timer file ----

[Unit]
Description={description_timer}
Requires={service_name}.service

[Timer]
Unit={service_name}.service
<OnCalendar=*-*-* *:*:00>

[Install]
WantedBy=timers.target


"""