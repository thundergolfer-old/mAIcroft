import unittest
from mock import patch
from contextlib import contextmanager
from io import StringIO

@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

"""
Use of the above

with captured_output() as (out, err):
    foo()
# This can go inside or outside the `with` block
output = out.getvalue().strip()
self.assertEqual(output, 'hello world!')
"""

from maicroft.core import process_social_user


@patch('maicroft.core.RedditUser', return_value="Not a user")
def test_process_social_user_reddit(mockRedditUser):
    user = process_social_user('some_username', 'reddit', prettyprint=False)
    assert "Not a user" == user

@patch('maicroft.core.TwitterUser', return_value="Not a twitter user")
def test_process_social_user_twitter(mockTwitterUser):
    user = process_social_user('some_twitter_id', 'twitter', prettyprint=False)
    assert "Not a twitter user" == user
