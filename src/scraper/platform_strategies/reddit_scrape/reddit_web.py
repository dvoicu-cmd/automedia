from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time


class RedditScrape:

    def __init__(self):
        self.driver = uc.Chrome()


    def scrape(self, subreddit, filter_type, post_type, num_scrolls, time_to_scroll, top_time='day'):
        """

        """

        # First do some syntax checks
        filter_types = ['hot', 'new', 'top', 'rising']
        top_time_ranges = ['hour', 'day', 'week', 'month', 'year', 'all']
        post_types = ['image', 'video', 'link', 'text']   # search for post-type attribute

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

        # Store array of download links
        download_links = []

        for post in shreddit_posts:
            pass






    def __scroll(self, wait_time):
        """

        :param wait_time:
        :return:
        """
        # One scroll -> give around 30 posts
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(wait_time)

