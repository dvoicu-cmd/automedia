from .publisher_formulas import PublisherFormulas
from .creator_formulas import CreatorFormulas
from .scraper_formulas import ScraperFormulas
from .central_formulas import CentralFormulas


class InterfaceFormula:
    def __init__(self):
        pass

    @staticmethod
    def create_formula(formula_type: str, formula_method: str, *args):
        match formula_type:
            case "creator":
                CreatorFormulas().create_formula(formula_method, *args)
            case "publisher":
                PublisherFormulas().create_formula(formula_method, *args)
            case "scraper":
                ScraperFormulas().create_formula(formula_method, *args)
            case "central":
                CentralFormulas().create_formula(formula_method, *args)
            case _:
                pass
