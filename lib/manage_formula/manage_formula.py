

class ManageFormula:
    """
    Class that manages formulaic python scripts that are ran by systemd
    """
    def __init__(self):

        self.template_top = """\
        # generate python script from ManageFormula class
        def main():
            # Common code and imports
            
            
            # User defined strategies
            {}
        """

        self.template_bottom = """\
            
            print("Script Successful")
            # end of main()
            
        # Main method call
        if __name__ == "__main__":
            main()
        
        """

    def append_code(self, code):
        format_code = ""
        format_code += f"    # User-defined strategy: {code}\n"
        self.template_top.format(format_code)
        self.template_top += "    {}\n"

    def save_generated_script(self, output_file_location):
        script_content = self.template_top
        script_content.format("")
        script_content += self.template_bottom

        with open(output_file_location, "w") as file:
            file.write(script_content)
