
from contextlib import closing
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
    with closing(InstaBot()) as bot:
        bot.login()

        if False:
            bot.follow_users([
                'beatcinema',
                'eatatpot',
                ])

        if True:
            bot.like_tags([
                'ootd',
                ],
                num=100)
