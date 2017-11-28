"""
File: twitter_marshal.py
Author: zrice
Github: github.com/zricethezav/twitter_keep
Description: download and marshal tweets into postgres
"""

import twitter
import click
import settings
logger = settings.logger


def get_tweets(handle, start_date, end_date):
    # TODO include options logic
    api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER_KEY,
                      consumer_secret=settings.TWITTER_CONSUMER_SECRET,
                      access_token_key=settings.TWITTER_ACCESS_KEY,
                      access_token_secret=settings.TWITTER_ACCESS_SECRET,
                      debugHTTP=False)

    statuses = api.GetUserTimeline(screen_name='realDonaldTrump')
    logger.info('Pulling %s timeline. From %s to %s', handle, start_date,
                end_date)
    for s in statuses:
        print s.text


@click.command()
@click.option('--handle', default=None, help='twitter handle to handle')
@click.option('--start_date', default=None, help='start date of tweets')
@click.option('--end_date', default=None, help='end date of tweets')
def main(handle, start_date, end_date):
    get_tweets(handle, start_date, end_date)


if __name__ == "__main__":
    main()
