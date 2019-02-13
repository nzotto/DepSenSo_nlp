"""
    Nicola Zotto APC1

    Import Twitter data from a specified accound
"""
## import dependencies
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta

## details for twitter application
consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""

## setup for tweetpy
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)

## get user_name from the website
user_name = ""

## optain Twiiter_User_Object (TUO)

TUO = auth_api.get_user(user_name)

## example data

name = TUO.name
screen_name = TUO.screen_name
description = TUO.description
total_number_of_tweets = str(TUO.statuses_count)
number_of_followed = str(TUO.friends_count)
number_of_followers = str(TUO.followers_count)
creation_date = item.created_at

## get user's timeline over the last month
## produce a dictionary entry ?

tweet_count = 0
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
    if hasattr(status, "text"):
        ## text content of the tweet
    if hasattr(status, "favorite_count"):
        ## number of times this status was favorited
    if hasattr(status, "retweet_count"):
        ## number of times this status was retweeted
    if hasattr(status, "in_reply_to_user_id_str"):
        ## user_id of the person being responded too
