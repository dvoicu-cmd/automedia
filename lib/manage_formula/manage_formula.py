import os


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
import cv2
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
    def delete_generated_script(service_name):
        """Static method to shortcut delete the py service script"""
        path = f"{os.getcwd()}/{service_name}.py"
        os.remove(path)

    @staticmethod
    def print_script_names():
        """Print all files in the py_service dir"""
        d = f"{os.getcwd()}"  # Directory
        return os.listdir(d)  # Return lmao

