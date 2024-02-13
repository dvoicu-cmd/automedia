from context import src
from context import lib
from src import *
from lib import *


"""
Wrapper functions
"""


def main():
    pg.verify_cfg()
    v1 = pg.main_menu("creator")
    if v1 == 'custom':

        # CUSTOM CREATOR FORMULA CREATION

        lines = []

        # Pick the canvas
        v2 = PickerPage(['NineBySixteen', 'SixteenByNine']).prompt()
        if v2 == 0:  # 9x16
            v3 = PickerPage(['High Resolution', 'Low Resolution'])
            if v3 == 0:
                lines.append("canvas = NineBySixteen('1080x1920')")
            else:
                lines.append("canvas = NineBySixteen('720x1280')")
        if v2 == 1:  # 16x9
            v3 = PickerPage(['High Resolution', 'Low Resolution'])
            if v3 == 0:
                lines.append("canvas = SixteenByNine('1080x1920')")
            else:
                lines.append("canvas = SixteenByNine('720x1280')")

        # # Apply edits
        # contd = True
        # while contd:
        #     PickerPage([''])


def create_creator_formula(py_service_name, code_lines: [str]):
    try:
        formula = ManageFormula()
        for line in code_lines:
            formula.append_code(line)
        formula.save_generated_script(py_service_name)
    except Exception as e:
        return e
    return 200


def delete_creator_formula(py_service_name):
    try:
        ManageFormula().delete_generated_script(py_service_name)
    except Exception as e:
        return e
    return 200



if __name__ == '__main__':
    main()

