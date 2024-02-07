# generate python script from ManageFormula class

# Common code and imports
from context import lib
from context import src
from lib import *
from src import *


def main():        
    # Lock the critical section.
    ManageService().lock()
    
    try:
        # User defined strategies
        x = 5
        print(x)

    except Exception as e:
        # If something goes wrong you need to unlock the critical section.
        ManageService().unlock()
        raise e
    
    # Unlock
    ManageService().unlock()
    
    print("Successfully Ran Service:")
    print(__file__)
    # end of main()


# Main method call
if __name__ == "__main__":
    main()

