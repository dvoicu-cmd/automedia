import os
import pdb
from datetime import date, timedelta
import re
from .upload import Upload
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from seleniumbase import Driver
from seleniumbase import SB
import seleniumbase.common.exceptions
from pyotp.totp import TOTP
import platform

from lib.webdriver_util.display_manager import DisplayManager



class YtUpload(Upload):
    """
    Class for uploading content to YouTube via YouTube studio.
    """

    def __init__(self, email, password, auth_secret, time_out=10, max_try=5):
        """
        Constructor
        Args:
            email (str): The email address for an account
            password (str): The password for the account
            auth_secret (str): The 32 character keys for the 2fa authentication code.
        """

        # Headless display management
        if platform.system() == "Linux":
            print("Linux detected, enabling virtual display.")
            # Need to have a virtual display for linux
            self.dm = DisplayManager()
            self.dm.activate_display()
        elif platform.system() == "Darwin":
            print("Mac detected, no virtual display needed.")
            pass

        # REMEMBER TO GET RID OF remote_debug WHEN PUSHING FOR PRODUCTION.
        # It spins up multiple debug instances and takes up too much memory on deployment machines.
        # If you have issues with multiple instances, you can type ps and kill the main chromium instance
        # Access on chrome this url: chrome://inspect
        # Here you can see the headless instance running and you can debug as needed. headless=True
        self.driver = Driver(uc=True)  # remote_debug="127.0.0.1:9222"
        # Selenium base's pageLoadStrategy is set to normal by default -> pages will fully load before you can interact.
        # https://seleniumbase.io/help_docs/how_it_works/#no-more-flaky-tests

        self.TIMEOUT = time_out
        self.MAX_TRY = max_try
        print("Attempting google login")
        self.__login_google(email, password, auth_secret)
        print("Object set up, google login success.")
        self.account_name = None
        self.title = "default"
        self.description = "default"
        self.tags = "video"
        self.for_kids = False
        self.paid_promo = False
        self.thumbnail_config = {"set_thumbnail": False, "path": None}
        self.schedule_config = {"schedule_upload": False, "schedule_time": None, "schedule_date": None}
        self.screenshot_path = "/"

    def set_title(self, title):
        """
        Sets the title of the upload
        Args:
            title (str): a string less than 100 characters.
        """
        # title has 100-character limit
        if not len(title) > 100:
            self.title = title

    def set_account(self, account_name):
        """
        setter for the brand account username.
        :param account_name:
        :return:
        """
        self.account_name = account_name

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


    def enable_schedule(self, schedule_time, schedule_date):
        """
        Configs exec_upload to schedule an upload
        :return:
        """
        if not self.is_valid_time_format(schedule_time):
            print("INVALID SCHEDULED TIME, SCHEDULE REMAINS DISABLED")
            return

        self.schedule_config["schedule_upload"] = True
        self.schedule_config["schedule_time"] = schedule_time
        self.schedule_config["schedule_date"] = schedule_date


    def disable_schedule(self):
        """
        Configs exec_upload to not schedule an upload
        :return:
        """
        self.schedule_config["schedule_upload"] = False
        self.schedule_config["schedule_time"] = None
        self.schedule_config["schedule_date"] = None

    def set_screenshot_location(self, log_path):
        if os.path.exists(log_path) and os.path.isdir(log_path):
            self.screenshot_path = log_path

    def take_screenshot(self):
        self.driver.get_screenshot_as_file()


    def exec_upload(self, file_path):
        """
        Executes the upload process given a specific file
        :param file_path: The file to upload
        """
        print(f"Init exec upload {file_path}")
        if not os.path.exists(file_path):
            print(f"YT fail on path: {file_path}")
            raise ValueError(f"P path does not exists: {file_path}")

        try:  # if anything goes wrong, you want to ensure that that driver closes so you don't spawn 50+ driver instances.

            # Change to the desired brand account.
            print(f"Selecting account: {self.account_name}")
            self.__change_account()
            print("Success, proceeding to upload...")

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
                i = 0
                # id='file-loader' The input for the file
                # e = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[3]/ytcp-thumbnails-compact-editor/div[3]/ytcp-thumbnails-compact-editor-uploader/ytcp-thumbnail-uploader/input'  # old headless tumbnail button.
                e = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[3]/ytcp-video-thumbnail-editor/div[3]/ytcp-video-custom-still-editor/div/ytcp-thumbnail-uploader/input'
                # e = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[3]/ytcp-video-thumbnail-editor/div[3]/ytcp-video-custom-still-editor/div/ytcp-thumbnail-uploader/ytcp-thumbnail-editor/div[1]/ytcp-ve/button'  # This is the button, not the specific input.
                while i < self.MAX_TRY:
                    try:
                        thumbnail_input = self.driver.find_element(by=By.XPATH, value=e)
                        thumbnail_input.send_keys(self.thumbnail_config["path"])
                        self.driver.sleep(self.TIMEOUT)
                        break
                    except Exception as e:
                        i = i + 1
                        if i == self.MAX_TRY:
                            print(f"Thumbnail kept throwing an err: {e}\n Make sure you have the thumbnail feature enabled on your account.")
                            break
                        print(f"Threw err: {e} \n attempt num:{i}")
                        self.driver.sleep(self.TIMEOUT)
                        continue

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
            try:
                e = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[6]/ytcp-form-input-container/div[1]/div/ytcp-free-text-chip-bar/ytcp-chip-bar/div/input'
                self.__wait_verify(e)
                self.driver.type(e, self.tags)
            except selenium.common.exceptions.NoSuchElementException:
                pass  # Just ignore tags, they are not that important if they brick.

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

            # If schedule is configured, schedule the upload.
            if self.schedule_config["schedule_upload"]:
                # press the button to open scheduler
                e = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[3]/div[1]/ytcp-icon-button'
                self.__wait_verify(e)
                drop_down_scheduler = self.driver.find_element(By.XPATH, e)
                drop_down_scheduler.click()

                # Open date drop down
                e = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[3]/div[2]/ytcp-visibility-scheduler/div[1]/ytcp-datetime-picker/div/div[1]/ytcp-text-dropdown-trigger/ytcp-dropdown-trigger/div/div[3]'
                self.__wait_verify(e)
                drop_down_date = self.driver.find_element(By.XPATH, e)
                drop_down_date.click()

                # Input the date
                # So when you start inputting the date value, the interface makes this overlay that covers the screen
                # This is like a hit box covering everything. Acts as the click off to deselect date selection.
                # To bypass this, as it was giving lots of issues, you need to have the uni code character for "ENTER"
                # This will clear off the barrier. Sending it as a seperate key does not work.
                e = '/html/body/ytcp-date-picker/tp-yt-paper-dialog/div/form/tp-yt-paper-input/tp-yt-paper-input-container/div[2]/div/iron-input/input'
                self.__wait_verify(e)
                schedule_date = self.schedule_config["schedule_date"]
                schedule_date = f"{schedule_date}\ue007"
                self.driver.type(e, schedule_date)

                # Input the time.
                e = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[3]/div[2]/ytcp-visibility-scheduler/div[1]/ytcp-datetime-picker/div/div[2]/form/ytcp-form-input-container/div[1]/div/tp-yt-paper-input/tp-yt-paper-input-container/div[2]/div/iron-input/input'
                self.__wait_verify(e)
                self.driver.type(e, self.schedule_config["schedule_time"])

                # Video is now scheduled for upload.

            # Click the publish button
            e = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[3]'
            publish_button = self.driver.find_element(By.XPATH, e)
            publish_button.click()

            print(f"Successfully uploaded: {file_path}")

            # Wait a little bit after upload
            self.driver.sleep(self.TIMEOUT*1.5)

            self.driver.refresh()

        except Exception as e:
            self.quit()
            raise e

        try:
            self.driver.switch_to.alert.accept()
        except selenium.common.exceptions.NoAlertPresentException:
            pass

    def exec_upload_linked_short(self):
        """
        Planned method to exec upload that links to the most recently uploaded video on the channel.
        Requires tier 3 channel verification.
        :return:
        """
        pass

    def __login_google(self, account, password, auto_secrete):
        """
        Function for automating the Google login and setting up client to main youtube studio landing page.
        """

        # Create yt_studio login
        self.driver.get("https://studio.youtube.com/")

        i = 0  # var to count num of retries

        # Define the specific pages and how to handle them.
        def email_page():
            self.__wait_verify('#identifierId')
            self.driver.uc_click('#identifierId', reconnect_time=0.5)
            self.driver.type('#identifierId', account)
            self.driver.uc_click('#identifierNext > div > button', reconnect_time=0.5)

        def password_page():
            self.__wait_verify('#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input')
            self.driver.uc_click('#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input', reconnect_time=0.5)
            self.driver.type('#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input', password)
            self.driver.uc_click('#passwordNext > div > button')

        def auth_2fa():
            self.__wait_verify('#totpPin')
            self.driver.uc_click('#totpPin', reconnect_time=0.5)
            totp_code = TOTP(auto_secrete)
            self.driver.type('#totpPin', totp_code.now())
            self.driver.uc_click('#totpNext > div > button')


        # Do init email and password page.
        while i < self.MAX_TRY:
            try:
                email_page()
                password_page()
                break
            except Exception as e:
                i = i + 1
                if i == self.MAX_TRY:
                    self.quit()
                    raise e
                print(f"Threw err: {e} \n attempt num:{i}")
                self.driver.sleep(self.TIMEOUT)
                self.driver.get("https://studio.youtube.com/")
                pass

        # Just wait a little bit, it gets weird here.
        self.driver.sleep(self.TIMEOUT)

        # If the current google account does not totp enabled it will continue to youtube studio
        current_url = self.driver.current_url  # Get the current

        # TOTP
        while i < self.MAX_TRY:
            try:  # If the current url is still the google page, then call the 2fa method to fill the code.
                if not current_url.startswith("https://www.youtube.com/"):
                    auth_2fa()
                    break
                else:  # Else that means your on the youtube studio page.
                    break
            except Exception as e:
                i = i + 1
                if i == self.MAX_TRY:
                    self.quit()
                    raise e
                print(f"Threw err: {e} \n attempt num:{i}")
                self.driver.sleep(self.TIMEOUT)
                self.driver.find_element('#totpNext > div > button').clear()
                continue

        # Just wait a little bit, you want to confirm that everything loads.
        self.driver.sleep(self.TIMEOUT)

        # if the current google account has multiple brand accounts it will go to a special prompt page.
        # If not your on the main YT studio page.
        current_url = self.driver.current_url  # Get the current url

        while i < self.MAX_TRY:
            try:
                if current_url.startswith("https://www.youtube.com/signin_prompt"):
                    # select the first brand account on the list. It will be swapped later.
                    e = "/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/ytd-channel-switcher-renderer/div[2]/div/ytd-account-item-section-renderer/div[2]/ytd-account-item-renderer[1]/tp-yt-paper-icon-item"
                    self.__wait_verify(e)
                    first_account = self.driver.find_element(By.XPATH, e)
                    first_account.click()
                    break
                else:
                    break
            except Exception as e:
                i = i + 1
                if i == self.MAX_TRY:
                    self.quit()
                    raise e
                print(f"Threw err: {e} \n attempt num:{i}")
                self.driver.refresh()


    def quit(self):
        self.driver.quit()
        try:
            self.dm.stop_display()
        except:
            pass

    @staticmethod
    def ls_days_ahead(n):
        """
        Gives the list of days in
        :param n:
        :return: List of days that are ahead of today's date.
        """
        output = []
        current_date = date.today()
        for i in range(n):
            future_date = current_date + timedelta(days=i + 1)
            str_future_date = future_date.strftime("%b %d, %Y")
            output.append(str_future_date)
        return output

    @staticmethod
    def is_valid_time_format(time_str):
        # Regular expression pattern to match the time format xx:xx YY
        pattern = r'^(0?[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$'

        # Match the input time string against the pattern
        if re.match(pattern, time_str):
            return True
        else:
            return False

    def __change_account(self):
        """
        Changes to the proper brand account when you are already logged into the yt studio page
        :return:
        """
        # Get to the list of the associated accounts.
        e = '/html/body/ytcp-app/ytcp-entity-page/div/ytcp-header/header/div/ytd-topbar-menu-button-renderer/button'
        self.__wait_verify(e)
        account_btn = self.driver.find_element(By.XPATH, e)
        account_btn.click()

        e = '/html/body/ytcp-app/ytcp-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer[1]/div[2]/ytd-compact-link-renderer[3]/a/tp-yt-paper-item'
        self.__wait_verify(e)
        switch_account = self.driver.find_element(By.XPATH, e)
        switch_account.click()

        e = '/html/body/ytcp-app/ytcp-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[4]/ytd-multi-page-menu-renderer/div[3]/div[1]/ytd-account-section-list-renderer/div[2]/ytd-account-item-section-renderer/div[2]'
        self.__wait_verify(e)
        div_list_accounts = self.driver.find_element(By.XPATH, e)

        # Grab the list of webelements containing the accounts
        list_accounts = div_list_accounts.find_elements(By.CSS_SELECTOR, '#channel-title')

        # Iterate through all elements and find the one with the matching string value
        account_to_switch_to = None
        for account in list_accounts:
            if account.text == self.account_name:
                account_to_switch_to = account
                break
        if not account_to_switch_to:
            raise ValueError(
                f"{self.account_name} is not a valid account name. Valid dir contents: \n\n{div_list_accounts.text}")

        # Then switch to that account
        account_to_switch_to.click()

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
                    print("MAX RETRY LIMIT REACHED, QUITING DRIVER.")
                    self.quit()
                    raise e
                print(f"Threw err: {e} \n attempt num:{i}")
                self.driver.sleep(self.TIMEOUT)
                continue
