"""

"""

import subprocess
from service_configurator.service_configurator import ServiceConfigurator


class CreateService:
    def __init__(self, service_name, python_file):
        """
        Constructor
        Args:
            service_name (str): The name of the service
            python_file (str): The name of the
        """
        self.service_name = service_name
        self.service_config = ServiceConfigurator()

    def execute(self):
        dict = self.service_config.read()
        # Write the service file

        # Write the timer file

        # Activate the service with subsystem



    def __activate_service(self):
        """
        Activates the service on the host computer
        :return:
        """

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




