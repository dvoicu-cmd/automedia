import requests
import os
import glob
import random
import string

# Maybe at a later point you can implement a cache system to store content if there is a failure to connect to central


class DownloadManager:
    """
    Manages all the downloads from the various strategies
    """

    def __init__(self, rand_length=5):
        # Make sure to create the downloader folder
        if not os.path.exists(f"{os.getcwd()}/downloads"):
            self.__init_dirs()
        self.__rand_length = rand_length
        self.__rand = self.__generate_random_string(self.__rand_length)

    def new_rand_id(self):
        """
        initializes a new random value
        """
        self.__rand = self.__generate_random_string(self.__rand_length)

    def get_rand_id(self):
        """
        gets the random id
        """
        return self.__rand

    def set_apply_rand_length(self, length):
        self.__rand_length = length
        self.__rand = self.__generate_random_string(length)

    def dl_list_of_links(self, links, content_type, name):
        """
        Downloads a list of links
        """
        for link in links:
            self.new_rand_id()
            self.dl_via_link(link, content_type, name)

    def dl_via_link(self, link, content_type, name):
        """
        Downloads audio, image, and video content
        """
        valid = ['audio', 'image', 'video']
        if content_type not in valid:
            raise ValueError(f"Invalid content type: {content_type}")

        # determine the file extension
        fs_extension = ''
        if content_type == 'audio':
            fs_extension = '.mp3'
        elif content_type == 'image':
            fs_extension = '.jpg'
        elif content_type == 'video':
            fs_extension = '.mp4'

        wd = f"{os.getcwd()}/downloads/{content_type}"

        response = requests.get(link)
        if response.status_code == 200:
            with open(f"{wd}/{self.__rand}_{name}{fs_extension}", "wb") as f:
                f.write(response.content)
        else:
            ProcessLookupError(f"Failed to download contents. Response code:{response.status_code}")

    def dl_list_of_text(self, text_list, name):
        for text in text_list:
            self.new_rand_id()
            self.dl_text(text, name)

    def dl_text(self, text, name):
        """
        Writes the string text into a file
        """
        wd = f"{os.getcwd()}/downloads/text"
        with open(f"{wd}/{self.__rand}_{name}.txt", "w") as f:
            f.write(text)

    def clear_all(self):
        """
        clears the contents of the download folder
        """
        self.clear_dir('text')
        self.clear_dir('audio')
        self.clear_dir('image')
        self.clear_dir('video')

    def clear_dir(self, dir_name):
        """
        Clears the directory
        """
        # Check input
        valid = ['text', 'audio', 'image', 'video']
        if dir_name not in valid:
            raise ValueError(f"Invalid directory input: {dir_name}")

        # Get the specific target files
        files = self.select_dir(dir_name)

        # Remove all the files
        for file in files:
            if os.path.isfile(file):
                os.remove(file)

    @staticmethod
    def select_dir(dir_name):
        """
        Returns all files in a dir name
        :param dir_name:
        :return:
        """
        wd = f"{os.getcwd()}/downloads/{dir_name}"
        pattern = os.path.join(wd, '*')
        files = glob.glob(pattern)
        return files

    @staticmethod
    def dl_root():
        return f"{os.getcwd()}/downloads"

    @staticmethod
    def __init_dirs():
        """
        Creates the required directories for storing the files
        :return:
        """
        # First the root, downloads
        wd = os.getcwd()
        os.mkdir(f"{wd}/downloads")
        wd = f"{wd}/downloads"
        # Now create the 4 categories
        os.mkdir(f"{wd}/text")
        os.mkdir(f"{wd}/audio")
        os.mkdir(f"{wd}/image")
        os.mkdir(f"{wd}/video")

    @staticmethod
    def __generate_random_string(length):
        # Using random.choices to generate a random string
        letters_and_digits = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(letters_and_digits) for _ in range(length))
        return random_string
