from urlparse import urlparse

import requests

from subreddits import subreddits_dict, ignore_text_subs, default_subs
from text_parser import TextParser

# Base class for comments and submissions
class Post(object):
    """
    A class for "posts" - a post can either be a submission or a comment.

    """

    def __init__(
        self, id, subreddit, text, created_utc, score, permalink, gilded
    ):
        # Post id
        self.id = id
        # Subreddit in which this comment or submission was posted
        self.subreddit = subreddit
        # For comments, the comment body and for submissions, the self-text
        self.text = text
        # UTC timestamp when post was created
        self.created_utc = created_utc
        # Post score
        self.score = score
        # Permalink to post
        self.permalink = permalink
        # Gilded
        self.gilded = gilded


class Comment(Post):
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


class Submission(Post):
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
