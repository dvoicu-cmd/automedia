"""
Class for that configures the location paths of the service files

Further reading on systemd timers: https://opensource.com/article/20/7/systemd-timers

paths.cfg should look like so:

[PATHS]
ServiceDirectoryPath=/{path that points to where all the service and timer files are located on machine}
PythonRuntimePath=/{path that points towards where the python runtime is located. Typically, in the bin}
PythonScriptsPath=/{path that points to all the specific execution scripts}
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
