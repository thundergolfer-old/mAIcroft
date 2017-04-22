from __future__ import print_function
import praw
from maicroft.private_settings import reddit_secret, reddit_client_id, reddit_redirect_uri


user_agent = "mAIcroft 0.1 by /u/thundergolfer"

reddit = praw.Reddit(user_agent=user_agent)

reddit.set_oauth_app_info(client_id=reddit_client_id,
                     client_secret=reddit_secret,
                     redirect_uri=reddit_redirect_uri)
refresh_token = "32129462-5lCQ6tLb50uPvaMVgLhmugPqq4w'"
reddit.refresh_access_information(refresh_token)

# get_authorize_url( state, scope, refreshable )
# state : string of choice that represents this client
# scope : see below for desired scope
# refreshable : is the access_token refreshable? True, False
url = reddit.get_authorize_url('uniqueKey', 'identity history mysubreddits', True)
import webbrowser
#webbrowser.open(url)

access_information = reddit.get_access_information(oauth_secret)
print(access_information)

# Swap from one authenticated user to another with :
# r.set_access_credentials(**access_information)

authd_user = reddit.get_me()
print(authd_user.name, authd_user.link_karma)

# Auth token lasts for 60 min
# To refresh, there is this command :
# r.refresh_access_information(access_information['refresh_token'])
# PRAW 3.2+ will attempt to automatically refresh the token


## DESIRED SCOPE

# history: Access my voting history and comments or submissions I’ve saved or hidden.
# identity: Access my reddit username and signup date
# mysubreddits : Access the list of subreddits I moderate,
#                contribute to, and subscribe to.
#
# OPTIONAL :
# read : Access posts, listings and comments through my account.
#        (for private subreddit viewiing)
