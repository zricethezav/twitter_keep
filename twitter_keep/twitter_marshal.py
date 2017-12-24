"""
File: twitter_marshal.py
Author: zrice
Github: github.com/zricethezav/twitter_keep
Description: download and marshal tweets into postgres
"""

import twitter
import click
import settings

api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER_KEY,
                  consumer_secret=settings.TWITTER_CONSUMER_SECRET,
                  access_token_key=settings.TWITTER_ACCESS_KEY,
                  access_token_secret=settings.TWITTER_ACCESS_SECRET,
                  debugHTTP=False)


def twitter_search(keyword, options=None):
    """
    Twitter search util, this little guy will auto adjust
    the ranges for your search terms.

    start_date and end_date must have the form %Y-%m-%d, we will compare
    these dates with the start and end of the results from the initial twitter
    search call as to how best to adjust the ranges/query
    """
    search_tweets = []
    last_tid = None
    while True:
        if not search_tweets:
            # initial query
            query = "q=%s&count=100&result_type=mixed" % keyword
        else:
            # query with until id limit to prevent duplicate downloads
            query = "q=%s&count=100&max_id=%s&result_type=mixed" % (
                    keyword, last_tid)

        results = api.GetSearch(raw_query=query)

        for r in results:
            print r.created_at
        last_tid = results[-1].id

        # maxdate TODO braek logic


def get_user(handle):
    return api.GetUser(screen_name=handle)


def get_tweets(handle, start_date, end_date):
    return api.GetUserTimeline(screen_name=handle)


@click.command()
@click.option('--keyword', default=None, help='keyword or topic to search for')
@click.option('--handle', default=None, help='twitter handle to handle')
@click.option('--start_date', default=None, help='start date of tweets')
@click.option('--end_date', default=None, help='end date of tweets')
def main(keyword, handle, start_date, end_date):
    # user = get_user(handle)
    # tweets = get_tweets(handle, start_date, end_date)
    #
    # update user table
    # insert_user(user)
    # insert_tweets(tweets)
    twitter_search(keyword=keyword, options=None)


if __name__ == "__main__":
    main()
