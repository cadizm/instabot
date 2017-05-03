
from contextlib import closing
import random
import time

from selenium.common.exceptions import WebDriverException

from instabot import InstaBot

import logging
logging.basicConfig(
    filename='instabot.log',
    level=logging.INFO,
    format='%(asctime)s %(filename)s:%(lineno)d %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    )
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    tags = [
        'travel',
        'igdaily',
        'picoftheday',
        'potd',
        'photooftheday',
        'vsco',
        'vscocam',
        'photography',
        'theta360',
        'dji',
        'mavicpro',
        'snow',
        'snowboarding',
        'porsche',
        'sigsauer',
    ]

    random.seed()
    random.shuffle(tags)

    while True:
        try:
            with closing(InstaBot()) as bot:
                bot.login()
                for tag in tags:
                    usernames = bot.like_tags([tag], num=100)
        except Exception as e:
            logger.error(e)
