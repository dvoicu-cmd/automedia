from .publisher_formulas import PublisherFormulas
from .creator_formulas import CreatorFormulas
from .scraper_formulas import ScraperFormulas
from lib.manage_formula.manage_formula import ManageFormula
from lib.cli_interface.page.input_pages import InputPage


class InterfaceFormula:
    def __init__(self):
        pass

    @staticmethod
    def create_formula(formula_type: str, formula_method: str, attr_map: dict):
        # Match cases would be a better use, but python 3.8 does not support such syntax :(
        # I'm forced to use 3.8 for my Mac dev environment as mariadb does not work.
        if formula_type == "creator":
            CreatorFormulas().create_formula(formula_method, attr_map)
        if formula_type == "publisher":
            PublisherFormulas().create_formula(formula_method, attr_map)
        if formula_type == "scraper":
            ScraperFormulas().create_formula(formula_method, attr_map)

    @staticmethod
    def formula_name(formula: ManageFormula, attr_map={}):
        """
        Calls a common input for formula naming. This is done so that the name attribute is consistent among all formulas.
        :return: String of the inputted name.
        """
        name = InputPage("Input the name of the formula").prompt(default_value=attr_map.get("formula_name"),
                                                                 default_lock=True)
        formula.spa("formula_name", f"{name}")
        return name
