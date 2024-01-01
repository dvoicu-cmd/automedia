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

    # --------- Public Methods --------- #

    def create(self, python_file, on_calendar_list):
        # Load the saved timer map
        self.timer_map.deserialize()

        # Attempt to add the file name as a key
        self.timer_map.new_timer_key(python_file)

        # Add on_calendar_list to the mapping
        self.timer_map.new_exec_time_value(python_file, on_calendar_list)

        # If the exec times are empty after adding
        exec_times = self.timer_map.get_exec_times(python_file)
        if exec_times is None:
            raise ValueError(f"The provided list: {on_calendar_list} conflicts with all the currently scheduled timers")

        # Write the service and timer files
        self.__write_service_file(python_file)
        self.__write_timer_file(python_file, exec_times)

        # Activate the service with subsystem
        self.__activate_service(python_file)

        # Save serialize the timer map
        self.timer_map.serialize()

    def delete(self, python_file):
        # Load the saved timer map
        self.timer_map.deserialize()

        # Delete the key on the map
        self.timer_map.delete_timer_key(python_file)

        # Stop services with subsystem
        self.__stop_service(python_file)

        # Delete files
        self.__delete_timer_file(python_file)
        self.__delete_service_file(python_file)

        return

    def create_paths_config(self, service_dir_path, python_runtime_path, python_scripts_path):
        """

        :param service_dir_path:
        :param python_runtime_path:
        :param python_scripts_path:
        :return:
        """
        self.service_config.write(service_dir_path, python_runtime_path, python_scripts_path)

    # --------- Service Control --------- #

    def __activate_service(self, py_file):
        """
        Activates the service on the host computer
        :return:
        """
        # Get that file location to the service files for the script before changing dirs for subprocess
        d = self.service_config.read()

        wd = os.getcwd()  # working directory
        self.__cd_to_desired_root(wd, 'src')  # cd until the src directory

        print(os.getcwd())

        # Change to dir with the bash files
        os.chdir('lib')
        os.chdir('manage_service')

        r = subprocess.run(['./start_service.sh', d.get('service_dir_path'), f"{py_file}.timer", f"{py_file}.service"])
        self.__verify_subprocess(r)

        # Change back working directory
        os.chdir(wd)

    def __stop_service(self, py_file):
        """
        Stops the service on the host computer
        :return:
        """
        wd = os.getcwd()  # working directory
        self.__cd_to_desired_root(wd, 'src')  # cd until the src directory

        # Change to dir with the bash files
        os.chdir('lib')
        os.chdir('manage_service')

        # Get that file location to the service files for the script
        d = self.service_config.read()
        r = subprocess.run(['./stop_service.sh', d.get('service_dir_path'), f"{py_file}.timer", f"{py_file}.service"])
        self.__verify_subprocess(r)

        # Change back working directory
        os.chdir(wd)

    # --------- Writing Files --------- #

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

    # --------- Deleting Files --------- #

    def __delete_service_file(self, py_file):
        path_dict = self.service_config.read()
        os.remove(f"{path_dict.get('service_dir_path')}/{py_file}.service")

    def __delete_timer_file(self, py_file):
        path_dict = self.service_config.read()
        os.remove(f"{path_dict.get('service_dir_path')}/{py_file}.timer")

    # --------- Helper Methods --------- #

    @staticmethod
    def __cd_to_desired_root(current_dir, desired_root):
        """
        Changes directories up the file system tree until you reach the desired directory
        :param current_dir:
        :param desired_root:
        :return:
        """
        while True:
            # Check if this is the current directory tree
            all = os.listdir(current_dir)
            if desired_root in os.listdir(current_dir):
                # You have reached the dir containing the desired directory. Append the desired dir to the current dir.
                current_dir = f"{current_dir}/{desired_root}"
                break

            # Move up a level in directory tree
            parent_dir = os.path.dirname(current_dir)

            # If you reach the fs root somehow
            if parent_dir == current_dir:
                raise ValueError(f"Reached the top most directory with out finding {desired_root}")

            # Update for next iteration
            current_dir = parent_dir

        # Update the current working directory of this file
        os.chdir(current_dir)

    @staticmethod
    def __verify_subprocess(self, r):
        if r.returncode == 1:
            raise BrokenPipeError("Something went wrong with the bash script")



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
