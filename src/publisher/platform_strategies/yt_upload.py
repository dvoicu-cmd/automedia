import os
from .upload import Upload

import selenium.common.exceptions
from selenium.webdriver.common.by import By
from seleniumbase import Driver
from pyotp.totp import TOTP

import pdb


class YtUpload(Upload):
    """
    Class for uploading content to YouTube via YouTube studio.
    """

    def __init__(self, email, password, auth_secret, time_out=5, max_try=5):
        """
        Constructor
        Args:
            email (str): The email address for an account
            password (str): The password for the account
            auth_secret (str): The 32 character keys for the 2fa authentication code.
        """

        self.driver = Driver(uc=True, headless=True)  # remote_debug="127.0.0.1:9222"
        self.TIMEOUT = time_out
        self.MAX_TRY = max_try
        pdb.set_trace()
        self.__login_google(email, password, auth_secret)
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
        Configures to set a thumbnail. Thumbnail files over 2mb will not be accepted.
        """
        if os.path.exists(img_path):
            # Get the size of the file in bytes
            file_size_in_bytes = os.path.getsize(img_path)

            # Convert bytes to megabytes
            file_size_in_mb = file_size_in_bytes / (1024 * 1024)

            # Only set true if the file size is less than 2mb
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
        Executes the upload process given a specific file
        """
        if not os.path.exists(file_path):
            raise ValueError(f"Video path does not exists: {file_path}")

        try:  # if anything goes wrong, you want to ensure that that driver closes so you don't spawn 50+ driver instances.

            # placeholder var to hold long XPaths
            e = ''

            # Checking for create icon if it is loaded.
            self.__wait_verify('#create-icon')
            self.driver.find_element(by=By.CSS_SELECTOR, value='#create-icon').click()

            # Click upload video
            self.__wait_verify('#text-item-0')
            self.driver.find_element(by=By.CSS_SELECTOR, value='#text-item-0').click()

            # Get the upload button
            e = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-uploads-file-picker/div/input'
            upload_button = self.driver.find_element(by=By.XPATH, value=e)

            # Send file to upload button
            upload_button.send_keys(file_path)

            # A wait for upload to finish before the move to the next page.
            self.__wait_verify('#basics')

            # Set the title
            e = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[1]/ytcp-video-title/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div'
            self.__wait_verify(e)
            self.driver.type(e, self.title)

            # Set the description
            e = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[2]/ytcp-video-description/div/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div'
            self.__wait_verify(e)
            self.driver.type(e, self.description)

            # Set thumbnail if configured to do so
            if self.thumbnail_config["set_thumbnail"]:
                try:
                    e = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[3]/ytcp-thumbnails-compact-editor/div[3]/ytcp-thumbnails-compact-editor-uploader/ytcp-thumbnail-uploader/input'
                    self.__wait_verify(e)
                    thumbnail_input = self.driver.find_element(by=By.XPATH, value=e)
                    thumbnail_input.send_keys(self.thumbnail_config["path"])
                except Exception as e:
                    print(f"Thumbnail threw an err: {e}\n Make sure you have the thumbnail feature enabled on your account.")
                    pass

            # Set not for kids
            if self.for_kids:
                e = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[5]/ytkc-made-for-kids-select/div[4]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[1]/div[1]'
                self.__wait_verify(e)
                self.driver.find_element(by=By.XPATH, value=e).click()
            else:
                e = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[5]/ytkc-made-for-kids-select/div[4]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[2]/div[1]'
                self.__wait_verify(e)
                self.driver.find_element(by=By.XPATH, value=e).click()

            # Toggle advanced settings
            e = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/div/ytcp-button'
            self.__wait_verify(e)
            self.driver.find_element(by=By.XPATH, value=e).click()

            # Wait and verify paid promotions loaded.
            e = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[1]/ytcp-checkbox-lit/div[1]'
            self.__wait_verify(e)

            # Enable paid promotions if configured to do so.
            if self.paid_promo:
                self.driver.find_element(by=By.XPATH, value=e).click()

            # Input tags,
            e = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[5]/ytcp-form-input-container/div[1]/div/ytcp-free-text-chip-bar/ytcp-chip-bar/div/input'
            self.__wait_verify(e)
            self.driver.type(e, self.tags)

            # get the next button and click it to move to next page.
            self.__wait_verify('#next-button')
            next_button = self.driver.find_element(By.CSS_SELECTOR, '#next-button')
            next_button.click()

            # Skip video elements
            self.__wait_verify('#next-button')
            next_button.click()

            # Skip checks
            self.__wait_verify('#next-button')
            next_button.click()

            # Wait for public button to load
            e = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[2]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[3]'
            self.__wait_verify(e)
            # Now click visibility to public
            public_button = self.driver.find_element(By.XPATH, e)
            public_button.click()

            # Click the publish button
            e = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[3]'
            publish_button = self.driver.find_element(By.XPATH, e)
            publish_button.click()

            # Wait a little bit after upload
            self.driver.sleep(self.TIMEOUT*1.5)

            self.driver.refresh()

        except Exception as e:
            self.driver.quit()
            raise e

        try:
            self.driver.switch_to.alert.accept()
        except selenium.common.exceptions.NoAlertPresentException:
            pass

    def select_account(self, account_name):
        # If you can see the avatar button, everything else should be present.
        self.__wait_verify('body > ytd-app > ytd-popup-container > tp-yt-paper-dialog')
        dir_list_accounts = self.driver.find_element(by=By.CSS_SELECTOR, value='#sections')
        list_accounts = dir_list_accounts.find_elements(by=By.CSS_SELECTOR, value='#channel-title')

        # Iterate through all elements and find the one with the matching string value
        account_to_switch_to = None
        for account in list_accounts:
            if account.text == account_name:
                account_to_switch_to = account
                break
        if not account_to_switch_to:
            raise ValueError(f"{account_name} is not a valid account name. Valid dir contents: \n\n{list_accounts.get_text()}")

        # Then switch to that account
        account_to_switch_to.click()

    def __login_google(self, account, password, auto_secrete):
        """
        Function for automating the Google login
        """

        # Create yt_studio login
        self.driver.get("https://studio.youtube.com/")

        i = 0  # var to count num of retries

        def email_page():
            self.driver.wait_for_element('#identifierId')
            self.driver.uc_click('#identifierId', reconnect_time=0.5)
            self.driver.type('#identifierId', account)
            self.driver.uc_click('#identifierNext > div > button', reconnect_time=0.5)

        def password_page():
            self.driver.wait_for_element('#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input')
            self.driver.uc_click('#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input', reconnect_time=0.5)
            self.driver.type('#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input', password)
            self.driver.uc_click('#passwordNext > div > button')

        def auth_2fa():
            self.driver.wait_for_element('#totpPin')
            self.driver.uc_click('#totpPin', reconnect_time=0.5)
            totp_code = TOTP(auto_secrete)
            self.driver.type('#totpPin', totp_code.now())
            self.driver.uc_click('#totpNext > div > button')

        while i < self.MAX_TRY:
            try:
                email_page()
                password_page()
                break
            except Exception as e:
                i = i + 1
                if i == self.MAX_TRY:
                    self.driver.quit()
                    raise e
                print(f"Threw err: {e} \n attempt num:{i}")
                self.driver.sleep(self.TIMEOUT)
                self.driver.get("https://studio.youtube.com/")
                pass

        # TOTP
        while i < self.MAX_TRY:
            try:
                auth_2fa()
                break
            except Exception as e:
                i = i + 1
                if i == self.MAX_TRY:
                    self.driver.quit()
                    raise e
                print(f"Threw err: {e} \n attempt num:{i}")
                self.driver.sleep(self.TIMEOUT)
                self.driver.find_element('#totpNext > div > button').clear()
                continue

    def quit(self):
        self.driver.quit()

    def __wait_verify(self, selector):
        i = 0  # counter for retrying
        # Initial wait and check to verify if an element exists
        # Sometimes the webpage moves too slow when initially loading so this loop provides a little safety net.
        while i < self.MAX_TRY:
            try:
                self.driver.wait_for_element(selector)
                self.driver.sleep(self.TIMEOUT)
                break
            except Exception as e:
                i = i + 1
                if i == self.MAX_TRY:
                    self.driver.quit()
                    raise e
                print(f"Threw err: {e} \n attempt num:{i}")
                self.driver.sleep(self.TIMEOUT)
                continue
