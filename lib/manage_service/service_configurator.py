"""
Class for that configures the location paths of the service files

paths.cfg should look like so:

[PATHS]
service_directory_path=/{path that points to where all the cron tab files are}
python_runtime_path=/{path that points towards where the python runtime is located. Typically, in the bin}
python_scripts_path=/{path that points to all the specific execution scripts}
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
            "service_dir_path": self.config['PATHS']['service_directory_path'],
            "python_runtime_path": self.config['PATHS']['python_runtime_path'],
            "python_scripts_path": self.config['PATHS']['python_scripts_path']
        }

        return output_dict

    def write(self, service_dir_path='/', python_runtime_path='/', python_scripts_path='/'):
        """
        Writes the paths.cfg file

        Args:
            service_dir_path: The path pointing towards the directory for loading cron files
            Typically located on linux machines in /etc/cron.d
            python_runtime_path: The path that points towards the python binary file. Typically located in /bin/python3
            python_scripts_path: The path that points to the python scripts that you wish to run schedule
        """
        # Set up the file
        self.config['PATHS'] = {}
        paths = self.config['PATHS']

        # write path params
        paths['service_directory_path'] = service_dir_path
        paths['python_runtime_path'] = python_runtime_path
        paths['python_scripts_path'] = python_scripts_path

        # Write the file
        with open('paths.cfg', 'w') as configfile:
            self.config.write(configfile)
