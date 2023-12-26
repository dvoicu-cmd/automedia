"""
Class for that configures the location paths of the service files

Note on timers: Timing needs to be done in a specific format
For OnUnitActiveSec:
s -> seconds, min -> minutes, d -> days, w -> weeks, M -> months, y -> years
ex: OnUnitActiveSec=5min activates the script every five minutes

Further reading on systemd timers: https://opensource.com/article/20/7/systemd-timers


paths.cfg should look like so:

[PATHS]
ExecStart=/{path of python3} /{file path of main.py}
WorkingDirectory=/{repository working directory file path}
[TIMERS]
OnBootSec={timer}
OnUnitActiveSec={timer}
OnCalendar={*-*-* *:*:00}

"""

import configparser


class ServiceConfigurator:
    def __init__(self):
        self.config = configparser.ConfigParser()

    def read(self):
        """
        Returns the contents of the paths.cfg file as a key value pair
        """
        # Attempt file read
        file = self.config.read('paths.cfg')

        if not file:
            raise FileNotFoundError(f'Failed to read paths.cfg file for obj: {self}')

        output_dict = {
            "exec_start": self.config['ExecStart'],
            "working_directory": self.config['WorkingDirectory'],
            "on_boot_sec": self.config['OnBootSec'],
            "on_unit_active_sec": self.config['OnUnitActiveSec'],
            "on_calendar": self.config['OnCalendar']
        }

        return output_dict

    def write(self, exec_start, working_directory, on_boot_sec, on_unit_active_sec, on_calendar):
        """
        Writes the paths.cfg file
        """
        # Set up the file
        self.config['PATHS'] = {}
        self.config['TIMERS'] = {}
        paths = self.config['PATHS']
        timers = self.config['TIMERS']

        # Write contents to obj
        # write path params
        paths['ExecStart'] = exec_start
        paths['WorkingDirectory'] = working_directory

        # write timer params
        timers['OnBootSec'] = on_boot_sec
        timers['OnUnitActiveSec'] = on_unit_active_sec
        timers['OnCalendar'] = on_calendar

        # Write the file
        with open('paths.cfg', 'w') as configfile:
            self.config.write(configfile)

