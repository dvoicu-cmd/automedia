from selenium.webdriver.common.by import By
from seleniumbase import Driver
import time


class RedditScrape:

    def __init__(self):
        self.driver = Driver(uc=True, headless=True)


    def scrape(self, subreddit, filter_type, post_type, num_scrolls: int, time_to_scroll: int, top_time='day'):
        """

        :param subreddit: The name of a subreddit to scrape
        :param filter_type: Specify a specific filter of posts 'hot', 'new', 'top', 'rising'
        :param post_type: Specify a specific type of post to scrape 'image', 'video', 'link', 'text'
        :param num_scrolls: The number of times you can scroll the page for scrapes
        :param time_to_scroll: The number of seconds you wait to after each scroll
        :param top_time: If the filter time is 'top', then you can select a range of which top times to pick from: 'hour', 'day', 'week', 'month', 'year', 'all'
        :return:
        """
        # First do some syntax checks
        filter_types = ['hot', 'new', 'top', 'rising']
        top_time_ranges = ['hour', 'day', 'week', 'month', 'year', 'all']
        post_types = ['image', 'video', 'link', 'text', 'gallery']   # search for post-type attribute

        if filter_type not in filter_types:
            raise ValueError("Invalid filter for subreddit")

        if filter_type == 'top':
            if top_time not in top_time_ranges:
                raise ValueError("Invalid top time range")

        if post_type not in post_types:
            raise ValueError("Invalid post type")

        # Now set the target url
        if filter_type == 'top':  # doing another check for clear code.
            target = f"https://www.reddit.com/r/{subreddit}/{filter_type}/?t={top_time}"
        else:
            target = f"https://www.reddit.com/r/{subreddit}/{filter_type}/"

        self.driver.get(target)

        # Scroll and load content
        while num_scrolls > 0:
            self.__scroll(time_to_scroll)
            num_scrolls -= 1

        # Get all the content labeled as posts. Does not pick up ads.
        shreddit_posts = self.driver.find_elements(By.TAG_NAME, 'shreddit-post')

        # Variable to return
        output = None

        # This is where you need to handle post types differently and extract the information you want
        if post_type == 'image':
            output = self.__image(shreddit_posts)
        if post_type == 'video':
            output = self.__video(shreddit_posts)
        if post_type == 'link':
            output = self.__link(shreddit_posts)
        if post_type == 'text':
            output = self.__text(shreddit_posts)
        if post_type == 'gallery':
            output = self.__gallery(shreddit_posts)
        if post_type == 'multi_media':
            output = self.__multi_media(shreddit_posts)


        return output


    # ---- specific strategies, too lazy to create separate classes for this ---- #
    @staticmethod
    def __image(posts: []):
        links = []
        for post in posts:
            post_type = post.get_attribute('post-type')
            if post_type == 'image':
                try:
                    img_elm = post.find_element(By.TAG_NAME, 'img')
                    link = img_elm.get_attribute('src')
                    links.append(link)
                except:
                    pass
        return links

    @staticmethod
    def __video(posts: []):
        links = []
        for post in posts:
            post_type = post.get_attribute('post-type')
            if post_type == 'video':
                try:
                    vid_elm = post.find_element(By.TAG_NAME, 'video')
                    link = vid_elm.get_attribute('src')
                    links.append(link)
                except:
                    pass
        return links

    @staticmethod
    def __link(posts: []):  # bruh who cares about link posts
        links = []
        for post in posts:
            post_type = post.get_attribute('post-type')
            if post_type == 'link':
                try:
                    vid_elm = post.find_element(By.TAG_NAME, 'video')
                    link = vid_elm.get_attribute('src')
                    links.append(link)
                except:
                    pass
        return links


    def __text(self, posts: []):  # Real shit

        full_post_links = []
        text_output = []

        # First loop to get the full post links
        for post in posts:
            post_type = post.get_attribute('post-type')
            if post_type == 'text':
                a_elm = post.find_element(By.TAG_NAME, 'a')
                link = a_elm.get_attribute('href')
                full_post_links.append(link)

        for full_post in full_post_links:
            build_string = ''

            # Navigate to post
            self.driver.get(full_post)

            # First try to click the read more button
            try:
                self.driver.find_element(By.XPATH, '/html/body/shreddit-app/dsa-transparency-modal-provider/div/main/shreddit-post/div[3]/div/button').click()
                time.sleep(1)
            except:
                pass

            # Get the post title
            title = self.driver.find_element(By.XPATH, '/html/body/shreddit-app/dsa-transparency-modal-provider/div/main/shreddit-post/h1')  # Title Text
            build_string = build_string + title.text + " "

            # Get the post content
            content = self.driver.find_element(By.XPATH, '/html/body/shreddit-app/dsa-transparency-modal-provider/div/main/shreddit-post/div[3]')
            build_string = build_string + content.text

            build_string = build_string.replace("\n", " ")

            # Add to list
            text_output.append(build_string)

        return text_output

    @staticmethod
    def __gallery(posts: []):
        for post in posts:
            pass

    @staticmethod
    def __multi_media(posts: []):
        for post in posts:
            pass


    def __scroll(self, wait_time):
        """
        Helper method the scrolls the window down
        :param wait_time:
        :return:
        """
        # One scroll -> give around 30 posts
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(wait_time)


