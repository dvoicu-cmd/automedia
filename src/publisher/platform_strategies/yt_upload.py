import configparser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

import pdb


class YtUpload:

    def __init__(self, email, password):
        """
        Constructor
        """
        self.driver = uc.Chrome()
        self.__login_google(email, password)

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

    def exec_upload(self):
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


    def select_account(self, account_name):
        # Get to the list of the associated accounts.
        self.driver.implicitly_wait(time_to_wait=3)
        account_btn = self.driver.find_element(By.XPATH, '/html/body/ytcp-app/ytcp-entity-page/div/ytcp-header/header/div/ytd-topbar-menu-button-renderer/button')
        account_btn.click()
        self.driver.implicitly_wait(time_to_wait=1)
        switch_account = self.driver.find_element(By.XPATH, '/html/body/ytcp-app/ytcp-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer[1]/div[2]/ytd-compact-link-renderer[3]/a/tp-yt-paper-item')
        switch_account.click()
        self.driver.implicitly_wait(time_to_wait=1)
        div_list_accounts = self.driver.find_element(By.XPATH, '/html/body/ytcp-app/ytcp-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[4]/ytd-multi-page-menu-renderer/div[3]/div[1]/ytd-account-section-list-renderer/div[2]/ytd-account-item-section-renderer/div[2]')

        # Grab the list of webelements containing the accounts
        list_accounts = div_list_accounts.find_elements(By.CSS_SELECTOR, '#channel-title')

        # Iterate through all elements and find the one with the matching string value
        account_to_switch_to = None
        for account in list_accounts:
            if account.text == account_name:
                account_to_switch_to = account
                break
        if not account_to_switch_to:
            raise ValueError(f"{account_name} is not a valid account name. Valid dir contents: \n\n{div_list_accounts.text}")

        # Then switch to that account
        account_to_switch_to.click()

        pdb.set_trace()


    def __login_google(self, account, password):
        """
        Function for automating the google login
        """
        # Create yt_studio login
        self.driver.get("https://studio.youtube.com/")
        self.driver.implicitly_wait(time_to_wait=1)

        # Login into google
        email_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input')
        email_button.send_keys(account)

        next_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button')
        next_button.click()

        self.driver.implicitly_wait(time_to_wait=2)

        password_input = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input')
        password_input.send_keys(password)

        self.driver.implicitly_wait(time_to_wait=2)

        pswd_button = self.driver.find_element(By.CSS_SELECTOR, '#passwordNext > div > button')
        pswd_button.click()

        self.driver.implicitly_wait(time_to_wait=3)

