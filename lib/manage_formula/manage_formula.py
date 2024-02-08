import os


class ManageFormula:
    """
    Class that manages formulaic python scripts that are ran by systemd
    """
    def __init__(self):
        self.template_top = """\
# generate python script from ManageFormula class

# Common code and imports
from context import lib
from context import src
from lib import *
from src import *


def main():        
    # Lock the critical section.
    ManageService().lock()
    
    try:
        # User defined strategies
{}"""   # Don't ask. Just whatever you do. DON'T TOUCH IT.

        self.template_bottom = """\
    except Exception as e:
        # If something goes wrong you need to unlock the critical section.
        ManageService().unlock()
        raise e
    
    # Unlock
    ManageService().unlock()
    
    print("Successfully Ran Service:")
    print(__file__)
    # end of main()


# Main method call
if __name__ == "__main__":
    main()

"""

    def append_code(self, code):
        self.template_top = self.template_top.format(f"        {code}\n")
        self.template_top += "{}"

    def save_generated_script(self, service_name):
        script_content = self.template_top.format("\n")
        script_content += self.template_bottom

        cwd = os.getcwd()

        if not os.path.exists(f"{cwd}/py_services"):
            os.mkdir("py_services")

        save_location = f"{cwd}/py_services/{service_name}.py"

        with open(save_location, "w") as file:
            file.write(script_content)

    @staticmethod
    def delete_generated_script(service_name):
        """Static method to shortcut delete the py service script"""
        path = f"{os.getcwd()}/py_services/{service_name}.py"
        os.remove(path)

    @staticmethod
    def print_script_names():
        """Print all files in the py_service dir"""
        d = f"{os.getcwd()}/py_services"  # Directory
        return os.listdir(d)  # Return lmao

