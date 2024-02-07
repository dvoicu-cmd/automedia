from lib.manage_formula.manage_formula import ManageFormula
import os

formula = ManageFormula()
formula.append_code("x = 5")
formula.append_code("print(x)")
formula.save_generated_script(f"{os.getcwd()}/YEAHHHH.py")
