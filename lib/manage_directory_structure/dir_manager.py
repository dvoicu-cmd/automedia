from abc import abstractmethod
import string
import random
import os
import glob
from shutil import rmtree


class DirManager:
    """
    Wrapper class to python's temp file module for encapsulating the creating of directories.
    """

    def __init__(self, rand_len=5):
        self.__init_dirs()
        self.rand_length = rand_len
        self.rand_hash = self.generate_random_string(rand_len)

    # ---- Manipulating Variables ---- #

    def new_rand_id(self):
        """
        initializes a new random value
        """
        self.rand_hash = self.generate_random_string(self.rand_length)

    def get_rand_id(self):
        """
        gets the random id
        """
        return self.rand_hash

    def set_apply_rand_length(self, length):
        """
        Sets and applies a new random hash given a length.
        :param length:
        :return:
        """
        self.rand_length = length
        self.rand_hash = self.generate_random_string(length)

    # ---- Util Methods ---- #

    def clear_dir(self, dir_name):
        """
        Clears the directory
        """
        # Get the specific target files
        files = self.select_dir(dir_name)

        # Remove all the files
        for file in files:
            if os.path.isfile(file):
                os.remove(file)

    @staticmethod
    def generate_random_string(length):
        # Using random.choices to generate a random string
        letters_and_digits = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(letters_and_digits) for _ in range(length))
        return random_string

    @staticmethod
    def select_dir(dir_path):
        """
        Returns all files in a dir name as a list
        :param dir_path: The path to the dir to select
        :return:
        """
        wd = dir_path
        pattern = os.path.join(wd, '*')
        files = glob.glob(pattern)
        return files

    def select_dir_one(self, dir_path):
        """
        Returns the file path in a dir with only one file in it
        :param dir_path:
        :return:
        """
        return self.select_dir(dir_path)[0]

    def create_tmp_dir(self, name=''):
        wd = f"{os.getcwd()}/output"
        tmp_dir = os.path.join(wd, f"{name}_{self.rand_hash}")
        os.mkdir(tmp_dir)
        return tmp_dir

    @staticmethod
    def read_text(file_location):
        with open(file_location, 'r') as f:
            file_contents = f.read()
        return file_contents

    @ staticmethod
    def cleanup(tmp_dir):
        rmtree(tmp_dir)

    @staticmethod
    def __init_dirs():
        """
        Creates the required directories for storing the files
        :return:
        """
        # Create two dirs: output and cache
        wd = os.getcwd()

        if not os.path.exists(f"{wd}/output"):
            # Output will contain any tmp directories to separates critical sections for each py_service
            os.mkdir(f"{wd}/output")
        if not os.path.exists(f"{wd}/cache"):
            # Cache will contain any left over dirs that have failed to be processed.
            os.mkdir(f"{wd}/cache")

    @abstractmethod
    def save_cache(self, *args):
        """
        Saves information to the cache directory using shutil.copytree and pickle. To be overwritten.
        :return:
        """
        pass

    @abstractmethod
    def load_cache(self, *args):
        """
        Loads the information from the cache directory. To be overwritten.
        :param args:
        :return:
        """
        pass

