"""

Note on timers: Timing needs to be done in a specific format
For OnUnitActiveSec:
s -> seconds, min -> minutes, d -> days, w -> weeks, M -> months, y -> years
ex: OnUnitActiveSec=5min activates the script every five minutes

"""

import subprocess
from .service_configurator import ServiceConfigurator


class ManageService:
    def __init__(self, service_name, python_file):
        """
        Constructor
        Args:
            service_name (str): The name of the service
            python_file (str): The name of the
        """
        self.service_name = service_name
        self.service_config = ServiceConfigurator()

    def write_path_config(self, exec_start='', working_directory='',  # Service file param
                          on_boot_sec='', on_unit_active_sec='', on_calendar='',  # Timer file param
                          abs_file_path=''):  # Location param
        """

        :param exec_start:
        :param working_directory:
        :param on_boot_sec:
        :param on_unit_active_sec:
        :param on_calendar:
        :param abs_file_path:
        :return:
        """
        self.service_config.write(exec_start, working_directory, on_boot_sec, on_unit_active_sec, on_calendar, abs_file_path)

    def create(self):
        # Write the service file

        # Write the timer file

        # Activate the service with subsystem
        return

    def delete(self):
        # Identify service file and timer file

        # Stop services with subsystem

        # Delete file

        return

    def __activate_service(self):
        """
        Activates the service on the host computer
        :return:
        """
        return

    def __stop_service(self):
        """

        :return:
        """
        return

    def __write_service_file(self):
        """
        Writes the .service file at the specified location
        :return:
        """
        return

    def __write_timer_file(self):
        """
        Writes the .timer file at the specified location
        :return:
        """
        return



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