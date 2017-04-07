
import os
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions

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

    def close(self):
        try:
            self.browser.delete_all_cookies()
            self.browser.close()
        except:
            pass

    def follow_users(self, usernames=None):
        for username in usernames:
            time.sleep(settings.FOLLOW_USER_SLEEP_SEC)
            self.browser.get('%s/%s' % (self.base_url, username))
            try:
                elem = self.browser.find_element_by_xpath(xpath.follow)
                if elem.text.lower() != 'following':
                    elem.click()
                    logger.info('Started following %s' % username)
                else:
                    logger.info('Already following %s' % username)

            except NoSuchElementException as e:
                logger.error(e)

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
