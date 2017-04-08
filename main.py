
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
        'ootn',
        'fashion',
        'fashionista',
        'fashiondiaries',
        'fashionblogger',
        'fashionphotography',
        'fashionphotographer',
        'lookbook',
        'wydwt',
        'style',
        'styleblogger',
        'instafashion',
        'igdaily',
        'picoftheday',
        'potd',
        'photooftheday',
        'photoshoot',
        'model',
        'models',
        'vsco',
        'vscocam',
        'shoot2kill',
        'photography',
        'afterhours',
    ]

    with closing(InstaBot()) as bot:
        bot.login()
        usernames = bot.like_tags(tags, num=100)
        bot.follow_users(random.sample(usernames, len(usernames)/2))
