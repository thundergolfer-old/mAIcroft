import sys
import string
try: import simplejson as json
except ImportError: import json
import tweepy
from tweepy import OAuthHandler


from private_settings import consumer_key, consumer_secret, access_token, access_secret
from maicroft_exceptions import NoDataError, UserNotFoundError

import private_settings

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

tweetAPI = tweepy.API(auth)

# List of all our tweets
# for tweet in tweepy.Cursor(tweetApi.user_timeline).items():
#     process_or_store(tweet._json)


class TwitterUser:
    """
    Models a twitter user object. Contains methods for processing
    comments and submissions.

    """

    # Set thresholds here
    #---------------------

    IMAGE_DOMAINS = ["imgur.com", "flickr.com"]
    VIDEO_DOMAINS = ["youtube.com", "youtu.be", "vimeo.com", "liveleak.com"]
    IMAGE_EXTENSIONS = ["jpg", "png", "gif", "bmp"]


    def __init__(self, user_id, json_data=None):
        # Populate username and about data
        self.user = tweetAPI.get_user(user_id)
        self.username = user_id

        self.comments = []
        self.submissions = []

        if not json_data:
            # Retrieve about
            self.about = self.get_about()
            if not self.about:
                raise UserNotFoundError
            # Retrieve comments and submissions
            self.tweets = self.get_tweets()
            self.comments = self.get_comments()
            self.retweets = self.get_retweets()
        else:
            data = json.loads(json_data)
            self.about = {
                "created_utc" : datetime.datetime.fromtimestamp(
                    data["about"]["created_utc"], tz=pytz.utc
                ),
                "link_karma" : data["about"]["link_karma"],
                "comment_karma" : data["about"]["comment_karma"],
                "name" : data["about"]["name"],
                "reddit_id" : data["about"]["id"],
                "is_mod" : data["about"]["is_mod"]
            }

    def __str__(self):
        return str(self.results())

    def get_about(self):
        return True

    def get_tweets(self):
        pass

    def get_comments(self):
        pass

    def get_retweets(self):
        pass

    def results(self):
        pass

if __name__ == '__main__':
    u = TwitterUser('jonobelotti_IO') # user_id
    print u.user
    #print TwitterUser('thundergolfer') # user_id
