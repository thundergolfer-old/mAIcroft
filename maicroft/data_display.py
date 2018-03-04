from __future__ import print_function

"""
Basic functions to aid in data understanding,
debugging, and presentation
"""


def display_user_tweets(twitter_user, limit=15):
    tweets = twitter_user.tweets
    for i, tweet in enumerate(tweets):
        print("{} : {}".format(i, tweet.text.encode('utf-8')))
        if i == limit:
            break
