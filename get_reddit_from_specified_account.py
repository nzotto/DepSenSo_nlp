"""
    Nicola Zotto

    Get reddit data using the reddit API "praw"
"""
import praw
from praw.models import MoreComments

## We need to create an app on this page:
## https://www.reddit.com/prefs/apps
## Should we create a dedicated reddit account?
def identification_reddit():
    """
    create instance for the data collection API
    :return: an instace of reddit that can be used to retrieve information on the user
    """
    ## details for reddit application
    app_id = 'lAFoUYMH9NC96w'
    app_secret = 'I_ekhjz-VCYkjOxJ4NhutP6yW2Q'
    app_name = 'DepSenTest'
    ## create the reddit instance /!\ ready_only
    reddit = praw.Reddit(client_id= app_id,
                         client_secret= app_secret,
                         user_agent= app_name)
    return res

def get_reddit_data(reddit, username):
    """
    Get data from the user's reddit account.
    we can only access the last 1000 comments posted by the targeted user (the limit is hard coded...)
    :param reddit: an instance of praw's reddit
    :param username: string, the reddit-username of the target
    :return: comment_list, a list of strings, the comments of the target
             submition_list, a list of tuple such as ('tittle', 'body'), the posts created by the target
    """
    redditor = reddit.redditor(username)

    comment_list = []
    ## parse through the comments
    for comment in redditor.comments.new(limit=None):
        comment_list.append(comment.body)
        ## We could also gather information on the comments replies, the parent coment's id (if the coment is a reply) or the post this comment is attached to.
    for submission in redditor.submissions.new(limit=None):
        submition_list.append((submission.title,submition.selftext))
    return comment_list, submition_list
