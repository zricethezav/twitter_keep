"""
File: settings.py
Author: zrice
Github: github.com/zricethezav/twitter_keep
Description: settings file
"""
import os
import logging

# TODO make logger class (make generic for reuse in other projects)
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-4s %(levelname)-4s: \033[95m%(message)s\033[0m')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

try:
    TWITTER_CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
    TWITTER_CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
    TWITTER_ACCESS_KEY = os.environ['TWITTER_ACCESS_KEY']
    TWITTER_ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']
except KeyError:
    logger.info("Exiting, please set your twitter api keys")
    exit()

# update
DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'vagrant',
    'password': '1securePassword',
    'database': 'twitter'
}
