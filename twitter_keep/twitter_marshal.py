"""
File: twitter_marshal.py
Author: zrice
Github: github.com/zricethezav/twitter_keep
Description: download and marshal tweets into postgres
"""

import twitter
import click
import settings
import models
import psycopg2
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER_KEY,
                  consumer_secret=settings.TWITTER_CONSUMER_SECRET,
                  access_token_key=settings.TWITTER_ACCESS_KEY,
                  access_token_secret=settings.TWITTER_ACCESS_SECRET,
                  debugHTTP=False)

meta = models.Base.metadata

db_conn = models.db_connect()
Session = sessionmaker(bind=db_conn)
session = Session()

def insert_user(user):
    users_table = meta.tables['users']
    print '\n\n\n\n\n'
    clause = users_table.insert().values(
        user_id=user.id,
        screen_name=user.screen_name,
        profile_image_url=user.profile_image_url,
        location=user.location,
        url=user.url,
        description=user.description,
        created_at=user.created_at,
        followers_count=user.followers_count,
        friends_count=user.friends_count,
        statuses_count=user.statuses_count,
        time_zone=user.time_zone,
        last_update='today'
    )
    result = db_conn.execute(clause)
    print result


def extract_point(geo):
    if not geo:
        return None, None
    elif geo['type'] == 'Point':
        return geo['coordinates'][0], \
               geo['coordinates'][1]


def insert_tweets(tweets):

    for tweet in tweets:
        lat, long = extract_point(tweet.geo)
        t = models.Tweet(
            tweet_id=tweet.id,
            text=tweet.text,
            created_at=tweet.created_at,
            geo_lat=lat,
            geo_long=long,
            user_id=tweet.user.id,
            screen_name=tweet.user.screen_name,
            retweet_count=tweet.retweet_count,
            favorite_count=tweet.favorite_count
        )

        for hashtag in tweet.hashtags:
            association = models.TweetHashtagAssociation()
            association.hashtag = models.Hashtag(
                hashtag_text=hashtag.text)
            t.hashtags.append(association)
        print '\n\n\n NOOOOO'
        session.add(t)
        session.commit()


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
