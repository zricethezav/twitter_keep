"""
File: twitter_marshal.py
Author: zrice
Github: github.com/zricethezav/twitter_keep
Description: download and marshal tweets into postgres
"""

# fuck it, just use sqlalchemy https://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/
import twitter
import click
import settings
import psycopg2

logger = settings.logger

sql_user_insert = """
        INSERT INTO users(
          user_id,
          screen_name,
          profile_image_url,
          location,
          url,
          description,
          created_at,
          followers_count,
          friends_count,
          statuses_count,
          time_zone,
          last_update
        ) VALUES (
          %s,
          %s,
          %s,
          %s,
          %s,
          %s,
          %s,
          %s,
          %s,
          %s,
          %s,
          %s
        ) ON CONFLICT DO NOTHING;"""

sql_tweet_insert = """
        INSERT INTO tweets(
          tweet_id,
          text,
          created_at,
          lat,
          long,
          user_id,
          screen_name,
          favorite_count,
          retweet_count,
          language
        ) VALUES (
          %s,
          %s,
          %s,
          %s,
          %s,
          %s,
          %s,
          %s,
          %s,
          %s
        );"""


api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER_KEY,
                  consumer_secret=settings.TWITTER_CONSUMER_SECRET,
                  access_token_key=settings.TWITTER_ACCESS_KEY,
                  access_token_secret=settings.TWITTER_ACCESS_SECRET,
                  debugHTTP=False)

conn = psycopg2.connect("dbname='twitter' "
                        "user='vagrant' "
                        "host='localhost' "
                        "password='1securePassword'")


def insert_user(user):
    cur = conn.cursor()
    cur.execute(sql_user_insert,
                    (
                        user.id,
                        user.screen_name,
                        user.profile_image_url,
                        user.location,
                        user.url,
                        user.description,
                        user.created_at,
                        user.followers_count,
                        user.friends_count,
                        user.statuses_count,
                        user.time_zone,
                        'today'
                    )
                )
    conn.commit()


def extract_point(geo):
    if not geo:
        return None, None
    elif geo['type'] == 'Point':
        return geo['coordinates'][0], \
               geo['coordinates'][1]


def insert_tweets(tweets):
    cur = conn.cursor()
    import json
    for tweet in tweets:
        print json.dumps(dir(tweet),indent=4)
        print tweet.user.id
        lat, long = extract_point(tweet.geo)
        for hashtag in tweet.hashtags:
            insert_hashtag(hashtag)
        print 'formatted tweet:'
        print sql_tweet_insert % (
                tweet.id,
                tweet.text,
                tweet.created_at,
                lat,
                long,
                tweet.user.id,
                tweet.user.screen_name,
                tweet.favorite_count,
                tweet.retweet_count,
                tweet.lang,
            )

        cur.execute(
            sql_tweet_insert,
            (
                tweet.id,
                tweet.text,
                tweet.created_at,
                lat,
                long,
                tweet.user.id,
                tweet.user.screen_name,
                tweet.favorite_count,
                tweet.retweet_count,
                tweet.lang,
            )
        )
    conn.commit()


def insert_hashtag(hashtag):
    pass


def get_user(handle):
    return api.GetUser(screen_name=handle)


def get_tweets(handle, start_date, end_date):
    return api.GetUserTimeline(screen_name=handle)


@click.command()
@click.option('--handle', default=None, help='twitter handle to handle')
@click.option('--start_date', default=None, help='start date of tweets')
@click.option('--end_date', default=None, help='end date of tweets')
def main(handle, start_date, end_date):
    user = get_user(handle)
    tweets = get_tweets(handle, start_date, end_date)

    # update user table
    insert_user(user)
    insert_tweets(tweets)


if __name__ == "__main__":
    main()
