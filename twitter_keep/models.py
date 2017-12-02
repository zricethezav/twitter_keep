from sqlalchemy.engine.url import URL
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import settings

Base = declarative_base()
Session = sessionmaker()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))


def create_tables(engine):
    """"""
    Base.metadata.create_all(engine)


class TweetHashtagAssociation(Base):
    __tablename__ = "tweets_hashtags"
    hashtag_text = Column(String, ForeignKey('hashtags.hashtag_text'),
                          primary_key=True)
    tweet_id = Column(BigInteger, ForeignKey('tweets.tweet_id'),
                      primary_key=True)
    hashtag = relationship('Hashtag', back_populates='tweets')
    tweet = relationship('Tweet', back_populates='hashtags')


class Tweet(Base):
    __tablename__ = 'tweets'
    tweet_id = Column(BigInteger, primary_key=True)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    geo_lat = Column(Float, nullable=True)
    geo_long = Column(Float, nullable=True)
    user_id = Column('user_id', ForeignKey('users.user_id'))
    screen_name = Column(String, nullable=False)
    favorite_count = Column(Integer, nullable=False)
    retweet_count = Column(Integer, nullable=False)
    keyword = Column(String, nullable=True)
    hashtags = relationship('TweetHashtagAssociation',
                            back_populates='tweet')


class User(Base):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True)
    screen_name = Column(String, nullable=False)
    profile_image_url = Column(String, nullable=False)
    location = Column(String, nullable=False)
    url = Column(String, nullable=True)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    followers_count = Column(Integer, nullable=False)
    friends_count = Column(Integer, nullable=False)
    statuses_count = Column(Integer, nullable=False)
    time_zone = Column(String, nullable=False)


class Hashtag(Base):
    __tablename__ = 'hashtags'
    hashtag_text = Column(String, primary_key=True)
    tweets = relationship('TweetHashtagAssociation',
                          back_populates='hashtag')


if __name__ == "__main__":
    # create_tables(db_connect())
    print dir(User)


