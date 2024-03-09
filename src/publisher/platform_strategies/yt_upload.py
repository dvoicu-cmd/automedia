import os
import time

import selenium.common.exceptions
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from pyotp.totp import TOTP

from .upload import Upload

import pdb


class YtUpload(Upload):
    """
    Class for uploading content to YouTube via YouTube studio.
    """

    def __init__(self, email, password, auth_secret):
        """
        Constructor
        Args:
            email (str): The email address for an account
            password (str): The password for the account
            auth_secret (str): The 32 character keys for the 2fa authentication code.
        """
        # Setting up headless mode to run without a gui and by systemctl scripts
        options = uc.ChromeOptions()

        # Remote debugger options for headless
        options.debugger_address = '127.0.0.1:9222'

        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--no-sandbox')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-setuid-sandbox')


        # user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15'
        # options.add_argument("--disable-blink-features=AutomationControlled")

        custom_user_agent_script = """
        Object.defineProperty(navigator, 'userAgent', {get: () => 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'});
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """

        # This don't work :(
        # options.add_argument(f"--user-agent={user_agent}")

        # https://stackoverflow.com/questions/71933644/getting-xvfb-to-work-in-jupyter-notebook-on-m1-mac
        # xquartz package contains xvfb for mac
        #os.environ["PATH"] += f"{os.pathsep}/opt/X11/bin"  # statement for specifying the binary

        print("Create uc")
        self.driver = uc.Chrome(headless=True, options=options)
        print("exec script")
        self.driver.execute_script(custom_user_agent_script)
        print("uc created")
        print(self.driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]) # prints the chrome version
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

        time.sleep(1)

        # Click create button
        self.driver.find_element(By.ID, 'create-icon').click()

        # Click upload video
        self.driver.find_element(By.ID, 'text-item-0').click()

        # Get the upload button
        upload_button = self.driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-uploads-file-picker/div/input')

        # Send file to upload button
        upload_button.send_keys(file_path)

        # Wait for next button to be seen. I know EC exists, but damn does it not work with this.
        time.sleep(3)

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
        time.sleep(3)

        # Skip video elements
        next_button.click()
        time.sleep(1)
        # Skip checks
        next_button.click()
        time.sleep(1)

        # Now click visibility to public
        public_button = self.driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[2]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[3]')
        public_button.click()
        time.sleep(1)

        # Click the publish button
        publish_button = self.driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[3]')
        publish_button.click()
        time.sleep(6)

        self.driver.refresh()

        try:
            self.driver.switch_to.alert.accept()
        except selenium.common.exceptions.NoAlertPresentException:
            pass

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
            if account.__text == account_name:
                account_to_switch_to = account
                break
        if not account_to_switch_to:
            raise ValueError(f"{account_name} is not a valid account name. Valid dir contents: \n\n{div_list_accounts.__text}")

        # Then switch to that account
        account_to_switch_to.click()


    def __login_google(self, account, password, auto_secrete):
        """
        Function for automating the Google login
        """

        # Create yt_studio login
        self.driver.get("https://studio.youtube.com/")
        # self.driver.get('accounts.google.com')

        # Tried injecting
        # self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        pdb.set_trace()

        # Login into google
        # Get email button
        email_button = self.driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/form/div[1]/section/div/div/div[1]/div/div/label/input')
        email_button.send_keys(account)
        time.sleep(2)

        # Next
        next_button = self.driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/form/div[2]/div/div[1]/button')
        next_button.click()
        time.sleep(2)

        pdb.set_trace()

        # Input password
        password_input = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input')
        password_input.send_keys(password)
        time.sleep(5)

        # Next
        password_button = self.driver.find_element(By.CSS_SELECTOR, '#passwordNext > div > button')
        password_button.click()
        time.sleep(5)

        # Now input 2fa

        # Set up elements to select
        two_fa = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section[3]/div/div/div[1]/div/div[1]/div/div[1]/input')
        save_device = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section[3]/div/div/div[2]/div[1]/div/div/div[1]/div/input')
        next_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button')

        # Toggle click, as you don't want the browser to remember the device as it messes with the alg
        save_device.click()
        # Send the 2fa code
        totp = TOTP(auto_secrete)
        two_fa.send_keys(totp.now())
        # Click next ASAP
        next_button.click()

        # There is a rare chance that inbetween sending the keys and clicking the button that the totp keys could have changed.
        # If that happens, god-damn, call me unlucky for the upload for that day.

        time.sleep(5)




