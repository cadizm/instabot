
from contextlib import closing
import random
import time

from instabot import InstaBot

import logging
logging.basicConfig(
    filename='instabot.log',
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    )


if __name__ == '__main__':
    tags = [
        'ootd',
        'bucketlist',
        'fashion',
        'fashionista',
        'picoftheday',
        'photography',
        'wydwt',
        'style',
        'styleblogger',
        'instafashion',
    ]

    with closing(InstaBot()) as bot:
        bot.login()
        usernames = bot.like_tags(tags, num=100)
        bot.follow_users(random.sample(usernames, len(usernames)/2))
