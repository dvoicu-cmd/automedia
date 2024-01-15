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
        self.title = "default"
        self.description = "default"
        self.tags = "default, default" # or a list. Comma seperated, figure that out.

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

    def exec_upload(self, file_path):
        """
        Executes the upload process
        """
        self.driver.implicitly_wait(time_to_wait=1)

        # Click create button
        self.driver.find_element(By.ID, 'create-icon').click()

        # Click upload video
        self.driver.find_element(By.ID, 'text-item-0').click()

        # Get the upload button
        upload_button = self.driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-uploads-file-picker/div/input')

        # Send file to upload button
        upload_button.send_keys(file_path)

        # Add expected condition, wait for it to load

        # Wait for the upload animation to play (usually takes 4 secs)
        self.driver.implicitly_wait(time_to_wait=8)
        # EC expected condition wait for next button to apear here

        # Set the title 100-character limit

        title_input = self.driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[1]/ytcp-video-title/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div')
        title_input.clear()
        title_input.send_keys(self.title)

        # Set the Description 5000 character limit
        desc_input = self.driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[2]/ytcp-video-description/div/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div')
        desc_input.clear()
        desc_input.send_keys(self.description)

        # Set thumbnail
        # First verify the number on an account

        # Set not for kids
        not_for_kids = self.driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[5]/ytkc-made-for-kids-select/div[4]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[2]/div[1]')
        not_for_kids.click()

        # Toggle advanced settings
        show_more = self.driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/div/ytcp-button')
        show_more.click()

        # Enable paid promotions
        toggle_paid_promo = self.driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[1]/ytcp-checkbox-lit/div[1]')
        toggle_paid_promo.click()

        # Input tags, Character count 500 (including commas)
        # err
        tags_input = self.driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[5]/ytcp-form-input-container/div[1]/div/ytcp-free-text-chip-bar/ytcp-chip-bar/div/input')
        tags_input.clear()
        tags_input.send_keys(self.tags)

        # get the next button and click it to move to next page.
        next_button = self.driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[2]')
        next_button.click()
        self.driver.implicitly_wait(time_to_wait=5)

        # Skip video elements
        next_button.click()
        self.driver.implicitly_wait(time_to_wait=5)
        # Skip checks
        next_button.click()
        self.driver.implicitly_wait(time_to_wait=5)

        # Now click visibility to public
        public_button = self.driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[2]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[3]')
        public_button.click()
        self.driver.implicitly_wait(time_to_wait=5)

        # Click the publish button
        publish_button = self.driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[3]')
        publish_button.click()
        self.driver.implicitly_wait(time_to_wait=5)

        # Close the final pop up
        close_button = self.driver.find_element(By.XPATH, '/html/body/ytcp-video-share-dialog/ytcp-dialog/tp-yt-paper-dialog/div[3]/ytcp-button')
        close_button.click()


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

