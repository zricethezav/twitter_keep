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


def twitter_search(keyword, start_date=None, end_date=None):
    """
    Twitter search util, this little guy will auto adjust
    the ranges for your search terms.

    start_date and end_date must have the form %Y-%m-%d, we will compare
    these dates with the start and end of the results from the initial twitter
    search call as to how best to adjust the ranges/query
    """
    print 'searching keywords: %s', keyword
    import json
    max_id = 0
    until_str = '2015-07-19'

    for i in xrange(2):
        results = api.GetSearch(raw_query="q=%s&count=100" % keyword)
        for r in results:
            print r.created_at
            print json.dumps(dir(r), indent=4)
        print json.dumps(dir(results), indent=4)


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
    #user = get_user(handle)
    #tweets = get_tweets(handle, start_date, end_date)

    # update user table
    # insert_user(user)
    # insert_tweets(tweets)
    twitter_search(keyword=keyword, options=None)


if __name__ == "__main__":
    main()
