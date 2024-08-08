from lib.manage_formula.manage_formula import ManageFormula

from lib.cli_interface.page.input_pages import InputPage
from lib.cli_interface.page.picker_pages import PickerPage
from lib.cli_interface.page.display_page import DisplayPage


class InterfaceFormulas:
    def __init__(self):
        pass

    # Common methods among formulas
    @staticmethod
    def formula_name(formula: ManageFormula, attr_map={}):
        """
        Calls a common input for formula naming. This is done so that the name attribute is consistent among all formulas.
        :return: String of the inputted name.
        """
        name = InputPage("Input the name of the formula").prompt(default_value=attr_map.get("formula_name"),
                                                                 default_lock=True)

        formula.spa("formula_name", f"{name}")

        # Do a quick search for the name if it exists and warn of overwriting.
        names = ManageFormula.read_all_formula_names()
        if name in names:
            DisplayPage().prompt("WARNING. Formula exists and continuing will overwrite the existing formula.")

        return name
