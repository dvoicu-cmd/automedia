import configparser
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

        # The config parser object
        self.properties = self.__init_config_obj()

        # Create the formula properties dir
        self.prop_dir = f"{os.getcwd()}/formula_properties"
        if not os.path.exists(self.prop_dir):
            os.mkdir(self.prop_dir)

    def append_code(self, code):
        self.template_top = self.template_top + '\n' + code

    def ap(self, code):
        """
        shorthand for append_code
        :param code:
        :return:
        """
        self.append_code(code)

    def save_generated_script(self, formula_name):
        script_content = self.template_top + '\n'
        script_content += self.template_bottom

        cwd = os.getcwd()

        save_location = f"{cwd}/{formula_name}.py"

        with open(save_location, "w") as file:
            file.write(script_content)

    @staticmethod
    def update_generated_script(formula_name: str):
        """
        update the contents of a generated formula by overwriting the formula.
        :param formula_name:
        :return:
        """
        # Get the formula
        path = f"{os.getcwd()}/{formula_name}.py"  # assumes py_services of current node



        pass

    @staticmethod
    def rename_generated_script(old_formula_name, new_formula_name):
        """
        Renames the formula
        :param old_formula_name:
        :param new_formula_name:
        :return:
        """
        old_path = f"{os.getcwd()}/{old_formula_name}.py"
        new_path = f"{os.getcwd()}/{new_formula_name}.py"
        # Get the formula.

        # Does not exist, raise exception.

        # If there is a conflicting name, raise an exception. Continue otherwise.

        # Change the name of the file

        # Change the name in the properties pickle

        # Check if there is a cron job by getting the timer map.

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


    # -------------- Properties Functionality --------------


    def add_property_attr(self, property_name, value):
        """
        Adds a property to the attributes in the formula's property.cfg file
        :param property_name: Name of the property (Key)
        :param value: Value of the property (Value)
        :return:
        """
        # Add the key and value
        self.properties['ATTRIBUTES'][property_name] = value

    def set_properties_type(self, node_type: str, strategy: str):
        """
        Sets the properties of the formula type identifiers of the formula. ie What formula was created for the purpose
        of being run again in the future.
        :param node_type:
        :param strategy:
        :return:
        """
        self.properties['TYPE']['node_type'] = node_type
        self.properties['TYPE']['strategy'] = strategy
        pass

    @staticmethod
    def read_properties_attr(formula_name: str):
        """
        Reads the attributes key values from the saved properties file of the given formula
        :return:
        """
        prop = ManageFormula.__read_properties_file(formula_name)
        print(f"prop read attributes of {formula_name}: {prop['ATTRIBUTES']}")
        return prop['ATTRIBUTES']

    @staticmethod
    def read_properties_type(formula_name: str):
        """
        Reads and returns the mapping of the
        :param formula_name:
        :return:
        """
        prop = ManageFormula.__read_properties_file(formula_name)
        output_dict = {
            "node_type": prop['TYPE']['node_type'],
            "strategy": prop['TYPE']['strategy']
        }
        return output_dict

    @staticmethod
    def __read_properties_file(formula_name: str):
        """
        Common method to load the property file of a formula
        :param formula_name:
        :return:
        """
        prop_dir = f"{os.getcwd()}/formula_properties/{formula_name}.cfg"
        config = configparser.ConfigParser()
        file = config.read(prop_dir)
        if len(file) == 0:
            raise FileNotFoundError('Failed to read config file')
        return config

    def __save_properties(self, formula_name: str):
        """
        Saves the built properties of a formula.
        :param formula_name: The name of the formula
        :return:
        """
        # Check if the properties dir exists in the py_services. If it does not exist, create it
        prop_dir = f"{os.getcwd()}/formula_properties"
        if not os.path.exists(prop_dir):
            os.mkdir(prop_dir)

        # Write the saved properties file
        with open(f'{prop_dir}/{formula_name}.cfg', 'w') as configfile:
            self.properties.write(configfile)

    @staticmethod
    def __remove_properties(formula_name: str):
        """
        Removes the properties file of a formula.
        :return:
        """
        prop_dir = f"{os.getcwd()}/formula_properties"
        os.rmdir(f"{prop_dir}/{formula_name}.cfg")

    @staticmethod
    def __rename_properties(old_formula_name, new_formula_name):
        """
        Renames the pickle file.
        :param old_formula_name:
        :param new_formula_name:
        :return:
        """
        pass

    @staticmethod
    def __update_property_attr(formula_name: str, updated_attributes: dict):
        prop = ManageFormula.__read_properties_file(formula_name)
        pass

    @staticmethod
    def __init_config_obj():
        config = configparser.ConfigParser()  # The config parser object
        config['TYPE'] = {}  # The type of strategy used
        config['ATTRIBUTES'] = {}  # The attributes inputted into a formula
        return config
