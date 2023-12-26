import configparser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class YtUpload:

    """
    obj variables
    """
    # --- Upload details ---
    content_path = None  # Location of the content on nfs server on central
    title = None  # Title of the content
    description = None  # The description
    config = None

    # ---


    def __init__(self, account, password):
        """
        Constructor
        """
        print("init youtube uploader")

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
