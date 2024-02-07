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
        Creates a systemd service that executes the inputted python script on the given onCalendar schedules.
        OnCalendar formatting: systemd timers use the format: {day of the week} {year}-{month}-{day} {hr}:{min}:{sec}.
        You can use the wild card * to signify every option for the calendar.
        ex1: execute script every day at 9 pm *-*-* 21:00:00
        ex2: execute script every monday at 9 am Mon *-*-* 09:00:00
        More documentation and specific can be found at:
        https://www.freedesktop.org/software/systemd/man/latest/systemd.time.html#
        and
        https://opensource.com/article/20/7/systemd-timers

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
        self.__write_service_file(python_file)
        self.__write_timer_file(python_file, on_calendar_list)

        # Activate the service with subsystem
        self.__activate_service(python_file)

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

        # Stop services with subsystem
        self.__stop_service(python_file)

        # Delete files
        self.__delete_timer_file(python_file)
        self.__delete_service_file(python_file)

    def lock(self):
        """
        Creates creates the lock file that forces other python services to sleep
        """
        path_dict = self.service_config.read()
        path_to_lock = f"{path_dict.get('service_dir_path')}/lock"
        if not os.path.exists(path_to_lock):
            with open(path_to_lock, 'w'):
                pass

    def unlock(self):
        """
        Deletes the lock file and allows for the next python services that awakes from sleep
        """
        path_dict = self.service_config.read()
        path_to_lock = f"{path_dict.get('service_dir_path')}/lock"
        if os.path.exists(path_to_lock):
            os.remove(path_to_lock)

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
        return self.timer_map.data

    # --------- Service Control --------- #

    def __activate_service(self, py_file):
        """
        Helper method that runs the bash scripts that enable and start the .service and .timer files for the python script

        Args:
            py_file (str): The string that contains the name of the python file excluding the .py extension in the current directory
        """
        # Get that file location to the service files for the script before changing dirs for subprocess
        d = self.service_config.read()

        wd = os.getcwd()  # working directory
        self.__cd_to_desired_root(wd, 'lib')  # cd until the lib directory

        print(os.getcwd())

        # Change to dir with the bash files
        os.chdir('manage_service')

        subprocess.run(['./start_service.sh', d.get('service_dir_path'), f"{py_file}.timer", f"{py_file}.service"])

        # Change back working directory
        os.chdir(wd)

    def __stop_service(self, py_file):
        """
        Helper method that runs the bash scripts that stop and disable the .service and .timer files for the python script

        Args:
            py_file (str): The string that contains the name of the python file excluding the .py extension in the current directory
        """
        # Get that file location to the service files for the script before changing dirs
        d = self.service_config.read()

        wd = os.getcwd()  # working directory
        self.__cd_to_desired_root(wd, 'src')  # cd until the src directory

        # Change to dir with the bash files
        os.chdir('lib')
        os.chdir('manage_service')
        
        # Run the bash files
        r = subprocess.run(['./stop_service.sh', d.get('service_dir_path'), f"{py_file}.timer", f"{py_file}.service"])
        # self.__verify_subprocess(r)

        # Change back working directory
        os.chdir(wd)

    # --------- Writing Files --------- #

    def __write_service_file(self, py_file):
        """
        Writes the .service file given the location found in the paths.cfg file

        Args:
            py_file (str): The string that contains the name of the python file excluding the .py extension in the current directory
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
                        f"ExecStartPre=/bin/bash -c 'while [[ -e {path_dict.get('service_dir_path')}/lock ]]; do sleep 5; done'\n"  # Checks if the lock exists
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
        Writes the .timer file given the location found in the paths.cfg file

        Args:
            py_file (str): The string that contains the name of the python file excluding the .py extension in the current directory
            on_calendar_list (list): on_calendar_list (list): A list of strings in the appropriate on calendar format. ex: ["*-*-* 21:00:00", "*-*-* 09:00:00"]

        """
        path_dict = self.service_config.read()

        file_content = (f"[Unit]\n"
                        f"Description=''\n"
                        f"Requires={py_file}.service\n"
                        f"\n"
                        f"[Timer]\n"
                        f"Unit={py_file}.service\n")

        # Append the on calendar elements
        for on_calendar_element in on_calendar_list:
            file_content = f"{file_content}OnCalendar={on_calendar_element}\n"

        # Add remaining items to file
        file_content = (f"{file_content}"
                        f"\n"
                        f"[Install]\n"
                        f"WantedBy=timers.target")

        with open(f"{path_dict.get('service_dir_path')}/{py_file}.timer", 'w') as f:
            f.write(file_content)

    # --------- Deleting Files --------- #

    def __delete_service_file(self, py_file):
        """
        Deletes the .service file given the location found in the paths.cfg file

        Args:
            py_file (str): The string that contains the name of the python file excluding the .py extension in the current directory
        """

        path_dict = self.service_config.read()
        os.remove(f"{path_dict.get('service_dir_path')}/{py_file}.service")

    def __delete_timer_file(self, py_file):
        """
        Deletes the .timer file given the location found in the paths.cfg file

        Args:
            py_file (str): The string that contains the name of the python file excluding the .py extension in the current directory
        """

        path_dict = self.service_config.read()
        os.remove(f"{path_dict.get('service_dir_path')}/{py_file}.timer")

    # --------- Helper Methods --------- #

    @staticmethod
    def __cd_to_desired_root(current_dir, desired_root):
        """
        Changes directories of the python runtime up the file system tree until you reach the desired directory

        Args:
            current_dir (str): The current working directory path.
            desired_root (str): The string name of the directory to cd up the file system to.
        """
        while True:
            # Check if this is the current directory tree
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
