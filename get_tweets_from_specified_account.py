"""
    Nicola Zotto APC1

    Import Twitter data from a specified accound
"""
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta

def identification_twitter():
    """
    create instance for the data collection API
    :return: an instace that can be used to retrieve information on the user
    """
    ## details for twitter application
    consumer_key=""
    consumer_secret=""
    access_token=""
    access_token_secret=""
    ## setup for tweetpy
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    auth_api = API(auth)
    return auth_api

def get_twitter_data(twitter, username):
    """
    Get data from the user's twitter account.
    :param twitter: an instance of tweepy'API
    :param username: string, the twitter-username of the target
    :return: tweet_count. int, the number of tweet colected
             status_list, a list of strings, the statuses posted by the user over the last month
    """
    ## optain Twiiter_User_Object (TUO)
    TUO = twitter.get_user(user_name)
    ## example data ...
##    name = TUO.name
##    screen_name = TUO.screen_name
##    description = TUO.description
##    total_number_of_tweets = str(TUO.statuses_count)
##    number_of_followed = str(TUO.friends_count)
##    number_of_followers = str(TUO.followers_count)
##    creation_date = item.created_at

    ## get user's timeline over the last month
    tweet_count = 0
    status_list = []
    end_date = datetime.utcnow() - timedelta(month=1)
    for status in Cursor(auth_api.user_timeline, id=target).items():
        ## exit loop after specified date.
        if status.created_at < end_date:
            break
        tweet_count += 1
        if hasattr(status, "entities"):
            ## the attribute entities contains hashtags, urls, symbols, media and user_mentions
        if hasattr(status, "text"):
            ## text content of the tweet
            status_list.append(status.text)
        if hasattr(status, "favorite_count"):
            ## number of times this status was favorited
            ## network analysys was dropped from the project
        if hasattr(status, "retweet_count"):
            ## number of times this status was retweeted
    return tweet_count, status_list
