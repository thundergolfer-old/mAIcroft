from __future__ import print_function
import sys
import string
import json
try: import simplejson as json
except ImportError: import json
import tweepy
from tweepy import OAuthHandler

from maicroft.maicroft_exceptions import NoDataError, UserNotFoundError
from maicroft.social_objects import Tweet, Location
try:
    from maicroft.private_settings import consumer_key, consumer_secret, access_token, access_secret
except ImportError:
    pass

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
        user = tweetAPI.get_user(user_id)  # throw this away because it contains unwanted data
        self.username = user.screen_name  # screen_name is unique, "name" is not

        self.tweets = []
        self.retweets = []
        self.shares = []

        if not json_data:
            # Retrieve about
            self.about = self.get_about(user)
            if not self.about:
                raise UserNotFoundError
            # Retrieve comments and submissions
            self.tweets = self.get_tweets()
            self.retweets = self.get_retweets()
            self.shares = self.get_shares()
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

    def get_about(self, user):
        """
        Return basic and general data about a twitter user
        """
        about = {
            "test" : "Hehdnff",
            "created_utc" : user.created_at, # format: datetime.datetime(2016,4,12,13,11,41)
            "name": user.name,
            "screen_name" : user.screen_name,
            "followers_count" : user.followers_count,
            "location" : user.location,
            "location_profile" : Location(user.profile_location),
            "profile_img" : user.profile_image_url
        }
        return about

    def get_tweets(self):
        """
        Returns a list of user's tweets
        """
        tweets = []
        for tweet in tweepy.Cursor(tweetAPI.user_timeline, id="jonobelotti_IO").items():
            t = self.get_tweet(tweet)
        tweets.append(t)
        return tweets

    def get_tweet(self,tweet):
        """

        """
        TWEET_BASE_ADDR = "https://twitter.com/statuses/" # for permalink

        text = tweet.text.encode("ascii", "ignore") # text (UTF-8)
        tweet_id = tweet.id_str.encode("ascii", "ignore")
        permalink = TWEET_BASE_ADDR + tweet_id
        coords = tweet.coordinates # coordinates
        created_utc = tweet.created_at # format: datetime.datetime(2011, 1, 1, 3, 15, 29)
        entities = tweet.entities # entities
        fave_count = tweet.favorite_count # favorite count
        self_faved = tweet.favorited # self favourited
        replyee_screenname = tweet.in_reply_to_screen_name # in_reply_to_screen_name
        replyee_id = tweet.in_reply_to_user_id_str.encode("ascii", "ignore") \
                     if tweet.in_reply_to_user_id_str else None
        replied_to_tweet_id = tweet.in_reply_to_status_id_str.encode("ascii", "ignore") \
                    if tweet.in_reply_to_status_id_str else None
        lang = tweet.lang if tweet.lang != "und" else None # lang
        place = tweet.place # places
        # 'quote tweets'
        retweet_count = tweet.retweet_count # retweet count
        self_retweeted = tweet.retweeted
        # is this tweet a retweet?
        try:
            retweeted_status = tweet.retweeted_status
        except AttributeError:
            retweeted_status = None

        t = Tweet(
            tweet_id, text,
            created_utc, fave_count,
            retweet_count,
            permalink,
            coords,
            entities,
            self_faved,
            replyee_screenname,
            replied_to_tweet_id,
            lang,
            place,
            self_retweeted,
            retweeted_status,
        )
        return t

    def get_retweets(self):
        """
        Return a list of user's retweets
        """
        retweets = []
        for tweet in self.tweets:
            if tweet.retweeted_status:
                retweet = self.get_tweet(tweet.retweeted_status)
                retweets.append(retweet)
        return retweets  # CAREFUL OF DOUBLE COUNTING A TWEET AND ITS RETWEET

    def get_shares(self):
        """
        Return a collection of lists of everything that a user has shared
        organized by content type (article, video, picture etc.)
        """
        pass

    def results(self):
        """
        Return a list of results after extracting information
        from user's data
        """

        # Twitterer has no data?
        if not (self.tweets or self.retweets or self.shares):
            raise NoDataError

        # Determine
        # Likes
        # Dislikes
        # Beliefs
        # Interests
        # Goals

if __name__ == '__main__':

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    tweetAPI = tweepy.API(auth)

    path = ""
    name = "twitter_user"
    sys.stdout = open(path + name + ".out", "w")
    u = TwitterUser('jonobelotti_IO')  # user_id
    print(u.about)
