import os
import pickle


class ManageFormula:
    """
    Class that manages formulaic python scripts that are ran by systemd
    """
    def __init__(self):
        self.template_top = """\
# generate python script from ManageFormula class

# Common code and imports
import os
import datetime
from context import cd_to_desired_root
from context import lib
from context import src
from lib import *
from src import *

start_time = datetime.datetime.now()
t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"------------ Starting Script: {t} ------------")  
# User defined code
"""

        self.template_bottom = """
# Current time
end_time = datetime.datetime.now()
elapsed_time = end_time - start_time
t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"------------ Finish Script: {t} ------------")
print(f"------------ Elapsed Time: {elapsed_time} ------------")
# end of main()
"""

    def append_code(self, code):
        self.template_top = self.template_top + '\n' + code

    def ap(self, code):
        """
        shorthand for append_code
        :param code:
        :return:
        """
        self.append_code(code)

    def save_generated_script(self, service_name):
        script_content = self.template_top + '\n'
        script_content += self.template_bottom

        cwd = os.getcwd()

        save_location = f"{cwd}/{service_name}.py"

        with open(save_location, "w") as file:
            file.write(script_content)

    @staticmethod
    def update_generated_script(service_name, *args):
        """
        Update the contents of a generated formula
        :param service_name:
        :return:
        """
        path = f"{os.getcwd()}/{service_name}.py"  # assumes py_services of current node
        pass

    @staticmethod
    def rename_generated_script(old_service_name, new_service_name):
        """
        Renames the formula
        :param old_service_name:
        :param new_service_name:
        :return:
        """
        path = f"{os.getcwd()}/{old_service_name}.py"
        # Get the formula.

        # Attempt to change the name

        # If there is a conflicting name, raise an exception

        # Else continue. Check if there is a cron job.
            # Get the timer map and see if the old name

        # If there is an entry, get the times, delete the timer then create a new one with the new name.
        pass

    @staticmethod
    def delete_generated_script(service_name):
        """Static method to shortcut delete the py service script"""
        path = f"{os.getcwd()}/{service_name}.py"
        os.remove(path)

    @staticmethod
    def print_script_names():
        """Print all files in the py_service dir"""
        d = f"{os.getcwd()}"  # Directory
        return os.listdir(d)  # Return lmao

    @staticmethod
    def __verify_properties_dir(self):
        pass
