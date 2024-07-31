

class CentralFormulas:

    def __init__(self):
        pass

    def create_formula(self, formula_method: str, *args):
        match formula_method:
            case "archive":
                self.archive()
                pass
            case _:
                pass

    @staticmethod
    def archive():
        """
        Create archive services
        :return:
        """
        pass
