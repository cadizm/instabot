
import os
import random
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys

from .exceptions import *
import settings
import xpath

import logging
logger = logging.getLogger(__name__)


class InstaBot(object):
    base_url = 'https://www.instagram.com'

    def __init__(self, implicit_wait=20, page_load_timeout=30):
        self.browser = Chrome(settings.CHROMEDRIVER_PATH, chrome_options=ChromeOptions())
        self.browser.implicitly_wait(implicit_wait)
        self.browser.set_page_load_timeout(page_load_timeout)

        self.liked = 0
        self.followed = 0

    def close(self):
        try:
            self.browser.delete_all_cookies()
            self.browser.close()
        except:
            pass

    def login(self, username=None, password=None):
        username = username or os.environ.get('INSTABOT_IG_USERNAME')
        password = password or os.environ.get('INSTABOT_IG_PASSWORD')

        if not username or not password:
            raise InvalidUsernamePasswordError

        self.browser.get(self.base_url)
        self.browser.find_element_by_xpath(xpath.login).click()
        self.browser.find_element_by_xpath(xpath.username).send_keys(username)
        self.browser.find_element_by_xpath(xpath.password).send_keys(password)
        self.browser.find_element_by_xpath(xpath.submit_login).click()

    def follow_users(self, usernames=None):
        """
        Follow all the users (don't pass `@')
        """
        for username in usernames:
            time.sleep(settings.FOLLOW_USER_SLEEP_SEC)
            self.browser.get('%s/%s' % (self.base_url, username))
            try:
                elem = self.browser.find_element_by_xpath(xpath.follow)
                if elem.text.lower() != 'following':
                    elem.click()
                    self.followed += 1
                    logger.info("Started following %s" % username)
                else:
                    logger.info("Already following %s" % username)

            except NoSuchElementException as e:
                logger.error(e)

    # TODO: add commenting to posts liked
    def like_tags(self, tags, num=100):
        """
        Like `num' number of posts when exploring hashtag (don't pass `#')

        A random sample of posts will be liked for a given tag
        Return the usernames of the posts liked
        """
        usernames = []
        for tag in tags:
            time.sleep(settings.LIKE_TAG_SLEEP_SEC)
            self.browser.get('%s/explore/tags/%s/' % (self.base_url, tag))
            time.sleep(settings.LIKE_TAG_SLEEP_SEC)
            self._load_more(max(1, num/10))

            # get the actual url's of images to like
            try:
                main = self.browser.find_element_by_tag_name('main')
            except NoSuchElementException as e:
                logger.error(e)

            links = main.find_elements_by_tag_name('a')
            urls = [link.get_attribute('href') for link in links]

            sample = random.sample(urls, min(num, len(links)))
            logger.info("Like sample size: %d" % len(sample))
            for url in sample:
                time.sleep(settings.LIKE_TAG_SLEEP_SEC)
                try:
                    self.browser.get(url)
                    elem = self.browser.find_element_by_xpath(xpath.like)
                    username = self.browser.find_element_by_xpath(xpath.profile_username).text
                except NoSuchElementException as e:
                    logger.error(e)
                    continue
                if elem.text.lower() == 'like':
                    elem.click()
                    self.liked += 1
                    usernames.append(username)

            logger.info("Liked %d/%d" % (self.liked, len(sample)))

        return usernames

    def _load_more(self, n=10):
        """
        Press "end" key `n' times to load more images
        """
        try:
            self.browser.find_element_by_xpath(xpath.load_more).click()
        except NoSuchElementException as e:
            logger.error(e)

        body = self.browser.find_element_by_tag_name('body')
        for _ in range(n):
            body.send_keys(Keys.END)
            time.sleep(settings.LOAD_MORE_SLEEP_SEC)
