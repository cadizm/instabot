
import os
import random
import time

from xvfbwrapper import Xvfb

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .exceptions import *
import settings
import xpath

import logging
logger = logging.getLogger(__name__)


class InstaBot(object):
    base_url = 'https://www.instagram.com'

    def __init__(self, implicit_wait=20, page_load_timeout=30):
        try:
            Xvfb().start()
        except EnvironmentError:
            pass

        options = ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-setuid-sandbox')

        self.driver = Chrome(settings.CHROMEDRIVER_PATH, chrome_options=options)
        self.driver.implicitly_wait(implicit_wait)
        self.driver.set_page_load_timeout(page_load_timeout)

        self.wait = WebDriverWait(self.driver, settings.WEB_DRIVER_WAIT_SEC)

        self.liked = 0
        self.liked_total_samples = 0
        self.followed = 0

    def close(self):
        try:
            self.driver.delete_all_cookies()
            self.driver.close()

            from subprocess import call
            call(['killall', 'Xvfb'])
            call(['killall', 'chromedriver'])
        except:
            pass

    def login(self, username=None, password=None):
        username = username or os.environ.get('INSTABOT_IG_USERNAME')
        password = password or os.environ.get('INSTABOT_IG_PASSWORD')

        if not username or not password:
            raise InvalidUsernamePasswordError

        logger.info("Logging in as: %s" % username)

        self.driver.get(self.base_url)
        self.driver.find_element_by_xpath(xpath.login).click()
        self.driver.find_element_by_xpath(xpath.username).send_keys(username)
        self.driver.find_element_by_xpath(xpath.password).send_keys(password)
        self.driver.find_element_by_xpath(xpath.submit_login).click()

    def follow_users(self, usernames=None):
        """
        Follow all the users (don't pass `@')
        """
        for username in usernames:
            time.sleep(settings.FOLLOW_USER_SLEEP_SEC)
            self.driver.get('%s/%s' % (self.base_url, username))
            try:
                elem = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath.follow)))
                if elem.text.lower() != 'following':
                    elem.click()
                    self.followed += 1
                    logger.info("Started following %s" % username)
                else:
                    logger.info("Already following %s" % username)

            except NoSuchElementException as e:
                logger.info(e)

            except Exception as e:
                logger.error(e)

    def like_tags(self, tags, num=100):
        """
        Like `num' number of posts when exploring hashtag (don't pass `#')

        A random sample of posts will be liked for a given tag
        Return the usernames of the posts liked
        """
        usernames = []
        for tag in tags:
            time.sleep(settings.LIKE_TAG_SLEEP_SEC)
            logger.info("Liking posts with tag: %s" % tag)
            self.driver.get('%s/explore/tags/%s/' % (self.base_url, tag))
            time.sleep(settings.LIKE_TAG_SLEEP_SEC)
            self._load_more(max(1, num/10))

            # get the actual url's of images to like
            try:
                main = self.driver.find_element_by_tag_name('main')
            except NoSuchElementException as e:
                logger.info(e)
                continue

            links = main.find_elements_by_tag_name('a')
            urls = [link.get_attribute('href') for link in links]

            sample = random.sample(urls, min(num, len(links)))
            self.liked_total_samples += len(sample)
            logger.info("Like sample size: %d" % len(sample))
            for url in sample:
                time.sleep(settings.LIKE_TAG_SLEEP_SEC)
                try:
                    self.driver.get(url)
                    elem = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath.like)))
                    username = self.driver.find_element_by_xpath(xpath.profile_username).text

                    if elem.text.lower() == 'like':
                        elem.click()
                        self.liked += 1
                        usernames.append(username)

                except NoSuchElementException as e:
                    logger.info(e)

            logger.info("Liked %d/%d" % (self.liked, self.liked_total_samples))

        return usernames

    def _load_more(self, n=10):
        """
        Press "end" key `n' times to load more images
        """
        body = self.driver.find_element_by_tag_name('body')
        for _ in range(n):
            body.send_keys(Keys.END)
            time.sleep(settings.LOAD_MORE_SLEEP_SEC)
