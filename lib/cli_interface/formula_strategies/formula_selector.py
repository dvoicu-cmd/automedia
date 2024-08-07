from .publisher_formulas import PublisherFormulas
from .creator_formulas import CreatorFormulas
from .scraper_formulas import ScraperFormulas


class FormulaSelector:
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
