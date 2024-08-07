import configparser
import os
from lib.manage_service.manage_service import ManageService


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
        """
        Saves the created formula. If the formula already exists, overwrite it instead
        :param formula_name:
        :return:
        """
        script_content = self.template_top + '\n'
        save_location = f"{ManageService().read_script_path()}/{formula_name}.py"

        with open(save_location, "w") as file:
            file.write(script_content)

        # Save the properties file
        self.__save_properties(formula_name)

    @staticmethod
    def rename_generated_script(old_formula_name, new_formula_name):
        """
        Renames the formula
        :param old_formula_name:
        :param new_formula_name:
        :return:
        """
        # ------------ formula part ------------
        # Get the formula.
        old_path = f"{ManageService().read_script_path()}/{old_formula_name}.py"
        new_path = f"{ManageService().read_script_path()}/{new_formula_name}.py"

        # Does not exist, raise exception.
        if not os.path.exists(old_path):
            raise FileNotFoundError

        # If there is a conflicting name, raise an exception. Continue otherwise.
        if os.path.exists(new_path):
            raise FileExistsError

        # Do the rename.
        os.rename(old_path, new_path)

        # Change the name in the properties cfg file
        ManageFormula().__update_property_attr(old_formula_name, "formula_name", new_formula_name)

        # Change the name of the file
        old_cfg = f"{ManageService().read_script_path()}/formula_properties/{old_formula_name}.cfg"
        new_cfg = f"{ManageService().read_script_path()}/formula_properties/{new_formula_name}.cfg"
        os.rename(old_cfg, new_cfg)

        # ------------ service part ------------

        # Check if there is a cron job by getting the timer map.
        s = ManageService()
        timer_map = s.timer_map  # get the deserialized mapping
        timer_map.deserialize()

        # Check that there are actual times.
        try:
            saved_times = timer_map.get_exec_times(f"{old_formula_name}")
        except ValueError:  # ie: timer does not exist.
            return  # Don't do the rest of the operations.

        # If there are time entries, delete the timer then create a map with new name with given times.
        s.delete(old_formula_name)
        s.create(new_formula_name, saved_times)

    @staticmethod
    def delete_generated_script(formula_name):
        """
        Static method to delete the py service script
        """
        path = f"{ManageService().read_script_path()}/{formula_name}.py"
        os.remove(path)
        ManageFormula.__remove_properties(formula_name)


    # -------------- Properties Functionality --------------


    def set_property_attr(self, attr_name: str, attr_value: str):
        """
        Adds a property to the attributes in the formula's property.cfg file
        :param attr_name: Name of the property (Key)
        :param attr_value: Value of the property (Value)
        :return:
        """
        self.properties['ATTRIBUTES'][f"{attr_name}"] = attr_value

    def spa(self, attr_name: str, attr_value: str):
        """
        shorthand of set_property_attr
        :return:
        """
        self.set_property_attr(attr_name, attr_value)

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
        attr_name = [option for option in prop['ATTRIBUTES']]  # Gets all the keys under attribute section.
        output_attr_map = {}
        for key in attr_name:
            output_attr_map[f"{key}"] = prop.get('ATTRIBUTES', key)
        return output_attr_map

    @staticmethod
    def __update_property_attr(formula_name: str, attr_name: str, new_attr_value: str):
        """
        Attempts to update a specified property value.
        """
        # Create a ConfigParser object
        config = configparser.ConfigParser()
        prop_dir = f"{ManageService().read_script_path()}/formula_properties"
        specific_property_cfg_file = f"{prop_dir}/{formula_name}.cfg"

        # Read the existing configuration file
        config.read(specific_property_cfg_file)

        # Check if the section and attribute exist before modifying
        if config.has_section('ATTRIBUTES') and config.has_option('ATTRIBUTES', f'{attr_name}'):
            # Update the specific attribute
            config.set('ATTRIBUTES', f'{attr_name}', f'{new_attr_value}')

            # Write the changes back to the configuration file
            with open(f'{specific_property_cfg_file}', 'w') as configfile:
                config.write(configfile)
        else:
            raise NameError


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
        prop_dir = f"{ManageService().read_script_path()}/formula_properties/{formula_name}.cfg"
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
        prop_dir = f"{ManageService().read_script_path()}/formula_properties"
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
        prop_dir = f"{ManageService().read_script_path()}/formula_properties"
        os.remove(f"{prop_dir}/{formula_name}.cfg")

    @staticmethod
    def __init_config_obj():
        config = configparser.ConfigParser()  # The config parser object
        config['TYPE'] = {}  # The type of strategy used
        config['ATTRIBUTES'] = {}  # The attributes inputted into a formula
        return config
