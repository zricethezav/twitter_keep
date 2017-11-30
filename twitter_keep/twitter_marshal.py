"""
File: twitter_marshal.py
Author: zrice
Github: github.com/zricethezav/twitter_keep
Description: download and marshal tweets into postgres
"""

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
          tweet_text,
          created_at,
          geo_lat,
          geo_long,
          user_id,
          screen_name,
          profile_image_url,
          is_rt
        ) VALUES (
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
        lat, long = extract_point(tweet.geo)
        """

        cur.execute(
            sql_tweet_insert,
            (
                tweet.id,
                tweet.text,
                tweet.created_at,
                lat,
                long,
                tweet.user_id,
                tweet.screen_name,
                tweet.hashtags, # maybe put this in a tweet_hashtag table
                tweet.favorite_count,
                tweet.current_user_retweet,
                tweet.in_reply_to_screen_name,
                tweet.in_reply_to_status_id,
                tweet.in_reply_to_user_id,
                tweet.lang,
                tweet.user_mentions,
                tweet.retweeted,
                tweet.retweet_count,
                tweet.retweeted_status,
                tweet.quoted_status,
                tweet.quoted_status_id,
                tweet.quoted_status_id_str
            )
        )
        """
        #print json.dumps(dir(tweet), indent=4)
        #print tweet
        print '\n'
        print tweet.text
        print tweet.hashtags
        print tweet.retweeted
        print tweet.retweet_count
        print tweet.favorite_count

def insert_hashtag():
    # TODO
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
