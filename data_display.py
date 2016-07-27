
from twitter_user import TwitterUser
from reddit_user import RedditUser

"""
Basic Social Content display functions to aid in data understanding,
debugging, and presentation
"""

def display_user_tweets(twitter_user, limit=15):
    """

    """
    tweets = twitter_user.tweets
    for i, tweet in enumerate(tweets):
        print str(i) + ": " + tweet.text.encode('utf-8')
        if i == limit:
            break

if __name__ == '__main__':
    user = TwitterUser('KimKardashian')
    display_user_tweets(user)
