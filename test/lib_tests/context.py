"""
The generic context file used to identify the project root and give access to all other project files when imported.
"""

import os
import sys


def cd_to_desired_root(current_dir, desired_root):
    """
    Changes directories of the python runtime up the file system tree until you reach the desired directory
    (This is taken from manage_service)

    Args:
        current_dir (str): The current working directory path.
        desired_root (str): The string name of the directory to cd up the file system to.
    """
    while True:
        # Check if this is the current directory tree
        if desired_root in os.listdir(current_dir):
            # You have reached the dir containing the desired directory. Append the desired dir to the current dir.
            current_dir = f"{current_dir}/{desired_root}"
            break

        # Move up a level in directory tree
        parent_dir = os.path.dirname(current_dir)

        # If you reach the fs root somehow
        if parent_dir == current_dir:
            raise ValueError(f"Reached the top most directory with out finding {desired_root}")

        # Update for next iteration
        current_dir = parent_dir

    # Update the current working directory of this file
    os.chdir(current_dir)


# Get this dir path
this_file = os.path.abspath(__file__)
this_dir = os.path.dirname(this_file)

# cd to project root
cd_to_desired_root(this_dir, 'automedia_backend')

# Append to path
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd())))

# change dir back
os.chdir(this_dir)
print(os.getcwd())

# Import src
import src

# Import lib
import lib

