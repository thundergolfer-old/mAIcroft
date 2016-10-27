from urlparse import urlparse

import requests

from maicroft.subreddits import subreddits_dict, ignore_text_subs, default_subs
from maicroft.text_parser import TextParser


# Base class for comments and submissions
class Post(object):
    """
    A class for "posts" - a post can either be a submission or a comment or tweet.
    """

    def __init__(
        self, id, text, created_utc, score, permalink
    ):
        # Post id
        self.id = id
        # For comments, the comment body and for submissions, the self-text
        # For Twitter, the tweet body
        self.text = text
        # UTC timestamp when post was created
        self.created_utc = created_utc
        # Post score,  or Tweet 'likes'
        self.score = score
        # Permalink to post
        self.permalink = permalink

class R_Post(Post):
    """
    A class for posts that come from Reddit
    """
    def __init__(
        self, id, subreddit, text, created_utc, score, permalink, gilded
    ):
        super(R_Post, self).__init__(
            id, text, created_utc, score, permalink
        )
        self.subreddit = subreddit # Subreddit in which comment or submission was posted
        self.gilded = gilded # Reddit posts and submissions can receive "Reddit Gold"

class Comment(R_Post):
    """
    A class for comments derived from Post.

    """

    def __init__(
        self, id, subreddit, text, created_utc, score,
        permalink, submission_id, edited, top_level, gilded
    ):
        super(Comment, self).__init__(
            id, subreddit, text, created_utc, score, permalink, gilded
        )
        # Link ID where comment was posted
        self.submission_id = submission_id
        # Edited flag
        self.edited = edited
        # Top-level flag
        self.top_level = top_level


class Submission(R_Post):
    """
    A class for submissions derived from Post.

    """

    def __init__(
        self, id, subreddit, text, created_utc, score,
        permalink, url, title, is_self, gilded, domain
    ):
        super(Submission, self).__init__(
            id, subreddit, text, created_utc, score, permalink, gilded
        )
        # Submission link URL
        self.url = url
        # Submission title
        self.title = title
        # Self post?
        self.is_self = is_self
        # Domain
        self.domain = domain


class Subreddit:
    """
    A class to represent a Reddit 'subreddit'. Used in Reddit user
    profile analysis.
    """

    def __init__(
        self, name, public_desc, sub_type, num_subs, over18,
        ignore_text, default_sub
    ):
        self.name = name
        self.public_desc = public_desc.decode('utf-8')
        self.type = sub_type
        self.num_subscribers = num_subs
        self.adult = over18
        self.ignore_text = ignore_text
        self.default_sub = default_sub


class Tweet(Post):
    """
    A class for Tweets derived from Post. Only contains data from the
    Twitter API that is relevant to the project.
    """

    def __init__(
        self, tweet_id, text, created_utc, faves, retweets,
        permalink, coords, entities, self_faved, replyee_screenname,
        replied_to_tweet_id, lang, place, self_retweeted, retweeted_status,
    ):
        super(Tweet, self).__init__(
            tweet_id, text, created_utc, faves, permalink
        )
        # Tweet specific feilds
        self.retweets = retweets
        self.coords = coords
        self.entities = entities if entities else None
        self.self_faved = self_faved
        self.replyee_screenname = replyee_screenname
        self.replied_to_tweet_id = replied_to_tweet_id
        self.lang = lang
        self.places = place
        self.self_retweeted = self_retweeted # is this interesting?
        self.retweeted_status = retweeted_status


class Location:

    def __init__(self, json_data):
        if json_data:
            self.country_code = json_data.get('country_code', None)
            self.country = json_data.get('country', None)
            self.full_name = json_data.get('full_name', None)
