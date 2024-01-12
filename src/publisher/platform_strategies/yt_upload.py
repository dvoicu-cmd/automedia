import configparser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import pdb


class YtUpload:

    """
    obj variables
    """
    # --- Upload details ---

    # ---


    def __init__(self, account, password, chrome_binary_path):
        """
        Constructor
        """
        options = Options()
        options.binary_location = chrome_binary_path
        options.add_argument("user-data-dir=$HOME/.config/google-chrome")
        # options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)

        # Create yt_studio login
        self.driver.get("https://studio.youtube.com/")
        self.driver.implicitly_wait(time_to_wait=2)
        usr_in = self.driver.find_element(By.TAG_NAME, 'input')
        usr_in.send_keys(account)
        next_btn = self.driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button')
        next_btn.click()


        pdb.set_trace()




    def load_config(self):
        """
        Loads the configuration
        """
        print("loads the config")

    def set_upload(self, content_path):
        """
        Sets the content of the upload
        Args:
            content_path (str): The directory path of the content
        """

    def set_title(self, title):
        """
        Sets the title of the upload
        Args:
            title (str): a string less than 100 char
        """

    def set_description(self, description):
        """
        Sets the description of the upload
        Args:
            description (str): a string less than 5000 char.
        """

    def __auto_login(self, driver):
        """
        Function for automating
        """

    def execute(self):
        """
        Executes the upload process
        """

        # --- First set up the webdriver ---
        options = Options()
        if(True): # If headless is configured, add headless option
            options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)

        # Set up link
        driver.get("studio.youtube.com")

        # --- Automate login
