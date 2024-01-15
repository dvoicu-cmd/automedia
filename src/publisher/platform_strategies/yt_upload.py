import os

import selenium.common.exceptions
import urllib3.exceptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc


class YtUpload:

    def __init__(self, email, password):
        """
        Constructor
        """
        self.driver = uc.Chrome()
        self.__login_google(email, password)
        self.title = "default"
        self.description = "default"
        self.tags = "default1,default2,default3"
        self.for_kids = False
        self.paid_promo = False
        self.thumbnail_config = {"set_thumbnail": False, "path": None}

    def set_title(self, title):
        """
        Sets the title of the upload
        Args:
            title (str): a string less than 100 characters.
        """
        # title has 100-character limit
        if not len(title) > 100:
            self.title = title

    def set_description(self, description):
        """
        Sets the description of the upload
        Args:
            description (str): a string less than 5000 characters.
        """
        # 5000 character limit
        if not len(description) > 5000:
            self.description = description

    def set_tags(self, tags):
        """
        Sets the tags for an upload
        Args:
            tags (str): A string with the words separated by commas. For example: tag1,tag2,tag3, ... tagN.
            Input can't be over 500 characters (including commas).
        """
        # character count 500 (including commas)
        if not len(tags) > 500:
            self.tags = tags

    def toggle_child_content(self):
        """
        Toggles the content to be for or not for kids
        """
        if self.for_kids:
            self.for_kids = False
        else:
            self.for_kids = True

    def toggle_paid_promotions(self):
        """
        Toggles the content to state if it has paid promotions
        """
        if self.paid_promo:
            self.paid_promo = False
        else:
            self.paid_promo = True

    def enable_thumbnail(self, img_path):
        """
        Configures to set a thumbnail. Thumbnail file can't be over 2mb
        """
        if os.path.exists(img_path):
            # Get the size of the file in bytes
            file_size_in_bytes = os.path.getsize(img_path)

            # Convert bytes to megabytes
            file_size_in_mb = file_size_in_bytes / (1024 * 1024)

            if file_size_in_mb <= 2:
                self.thumbnail_config["set_thumbnail"] = True
                self.thumbnail_config["path"] = img_path

    def disable_thumbnail(self):
        """
        Configures to not upload a thumbnail
        """
        self.thumbnail_config["set_thumbnail"] = False
        self.thumbnail_config["path"] = None

    def exec_upload(self, file_path):
        """
        Executes the upload process
        """
        if not os.path.exists(file_path):
            raise ValueError(f"Video path does not exists: {file_path}")

        self.driver.implicitly_wait(time_to_wait=1)

        # Click create button
        self.driver.find_element(By.ID, 'create-icon').click()

        # Click upload video
        self.driver.find_element(By.ID, 'text-item-0').click()

        # Get the upload button
        upload_button = self.driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-uploads-file-picker/div/input')

        # Send file to upload button
        upload_button.send_keys(file_path)

        # Wait for next button to be seen
        # WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[2]')))
        self.driver.implicitly_wait(time_to_wait=10)

        # Set the title
        title_input = self.driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[1]/ytcp-video-title/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div')
        title_input.clear()
        title_input.send_keys(self.title)

        # Set the description
        desc_input = self.driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[2]/ytcp-video-description/div/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div')
        desc_input.clear()
        desc_input.send_keys(self.description)

        # Set thumbnail if configured to do so
        if self.thumbnail_config["set_thumbnail"]:
            thumbnail_input = self.driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[3]/ytcp-thumbnails-compact-editor/div[3]/ytcp-thumbnails-compact-editor-uploader/ytcp-thumbnail-uploader/input')
            thumbnail_input.send_keys(self.thumbnail_config["path"])

        # Set not for kids
        if self.for_kids:
            for_kids = self.driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[5]/ytkc-made-for-kids-select/div[4]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[1]/div[1]')
            for_kids.click()
        else:
            not_for_kids = self.driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[5]/ytkc-made-for-kids-select/div[4]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[2]/div[1]')
            not_for_kids.click()

        # Toggle advanced settings
        show_more = self.driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/div/ytcp-button')
        show_more.click()

        # Enable paid promotions if configured to do so.
        if self.paid_promo:
            toggle_paid_promo = self.driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[1]/ytcp-checkbox-lit/div[1]')
            toggle_paid_promo.click()

        # Input tags,
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
        self.driver.implicitly_wait(time_to_wait=15)

        self.driver.find_element(By.XPATH, '/html/body/ytcp-uploads-still-processing-dialog/ytcp-dialog/tp-yt-paper-dialog/div[3]/ytcp-button').click()

    def select_account(self, account_name):
        # Get to the list of the associated accounts.
        self.driver.implicitly_wait(time_to_wait=5)
        account_btn = self.driver.find_element(By.XPATH, '/html/body/ytcp-app/ytcp-entity-page/div/ytcp-header/header/div/ytd-topbar-menu-button-renderer/button')
        account_btn.click()
        self.driver.implicitly_wait(time_to_wait=5)
        switch_account = self.driver.find_element(By.XPATH, '/html/body/ytcp-app/ytcp-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer[1]/div[2]/ytd-compact-link-renderer[3]/a/tp-yt-paper-item')
        switch_account.click()
        self.driver.implicitly_wait(time_to_wait=5)
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

