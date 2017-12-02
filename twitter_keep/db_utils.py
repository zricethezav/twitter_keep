import models
from sqlalchemy.orm import sessionmaker

meta = models.Base.metadata
db_conn = models.db_connect()
Session = sessionmaker(bind=db_conn)
session = Session()

def insert_user(user):
    user = models.User(
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
    session.merge(user)
    session.commit()


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
        session.add(t)
        session.commit()
